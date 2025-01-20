import { exec } from "child_process";
import { promisify } from "util";
import fs from "fs/promises";
import path from "path";
import getConfig from "./unlighthouse.config";
import { parse } from "json2csv"; // Biblioteca para criar CSV
const execPromise = promisify(exec);

export async function POST(req) {
  try {
    const body = await req.json(); // Lê o corpo da requisição
    const { sites } = body; // Recebe um array de URLs do corpo da requisição

    if (!Array.isArray(sites) || sites.length === 0) {
      return new Response(
        JSON.stringify({ error: "Forneça uma lista válida de sites." }),
        { status: 400, headers: { "Content-Type": "application/json" } }
      );
    }

    const results = [];
    const baseOutputDir = path.resolve(process.cwd(), "reports");

    for (const siteUrl of sites) {
      try {
        const startTime = Date.now();
        const config = getConfig(siteUrl, "desktop");
        const tempConfigPath = path.resolve("unlighthouse.config.temp.ts");
        const configContent = `module.exports = ${JSON.stringify(
          config,
          null,
          2
        )};`;

        await fs.writeFile(tempConfigPath, configContent, "utf-8");

        const command = `npx unlighthouse-ci --config-file ${tempConfigPath} --urls / --reporter json --output-path ${baseOutputDir}`;
        const { stdout, stderr } = await execPromise(command);

        if (stdout) console.log("Saída:", stdout);
        if (stderr) console.error("Erro:", stderr);

        const jsonFilePath = path.join(baseOutputDir, "ci-result.json");
        const fileData = await fs.readFile(jsonFilePath, "utf-8");
        const result = JSON.parse(fileData)[0];

        const endTime = Date.now();
        const analysisTime = (endTime - startTime) / 1000; // Tempo em segundos

        results.push({
          siteUrl,
          performance: result.performance || null,
          accessibility: result.accessibility || null,
          bestPractices: result["best-practices"] || null,
          seo: result.seo || null,
          analysisTime,
        });

        await fs.unlink(tempConfigPath);
      } catch (error) {
        console.error(`Erro ao processar ${siteUrl}:`, error.message);
        results.push({ siteUrl, error: error.message });
      }
    }

    // Converte os resultados em CSV
    const csv = parse(results, {
      fields: [
        "siteUrl",
        "performance",
        "accessibility",
        "bestPractices",
        "seo",
        "analysisTime",
      ],
    });

    // Salva o arquivo CSV
    const csvPath = path.resolve(process.cwd(), "analysis-results.csv");
    await fs.writeFile(csvPath, csv, "utf-8");

    return new Response(
      JSON.stringify({
        message: "Análise concluída",
        csvPath,
        results,
      }),
      {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }
    );
  } catch (error) {
    console.error("Erro geral:", error.message);
    return new Response(
      JSON.stringify({ error: "Erro interno do servidor", details: error.message }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
}
