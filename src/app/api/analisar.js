// pages/api/analisar.js
import { PrismaClient } from "@prisma/client";
import { exec } from "child_process";
import { promisify } from "util";
import fs from "fs/promises";
import path from "path";
import getConfig from "../../pages/api/unlighthouse.config";
import { saveAnalysisToDB } from "../../lib/saveAnalysis";
import { translate } from "./translate"; // Importa a função de tradução
const execPromise = promisify(exec);

const prisma = new PrismaClient();

export default async function handler(req, res) {
  if (req.method !== "GET") {
    return res.status(405).json({ error: "Método não permitido, use GET" });
  }

  const { siteUrl, device = "desktop" } = req.query;

  if (!siteUrl) {
    return res.status(400).json({ error: 'Parâmetro "siteUrl" é obrigatório' });
  }

  const site = await prisma.site.findUnique({
    where: { url: siteUrl },
  });

  if (!site) {
    return res
      .status(404)
      .json({ error: "Site não encontrado no banco de dados." });
  }

  // Define o diretório base de saída
  const baseOutputDir = path.resolve(process.cwd(), "reports");
  const tempConfigPath = path.resolve("unlighthouse.config.temp.ts");
  const jsonFilePath = path.join(baseOutputDir, "ci-result.json");

  try {
    // Obtemos a configuração dinâmica com a URL e o dispositivo
    const config = getConfig(siteUrl, device);

    // Escreve a configuração no arquivo temporário
    const configContent = `module.exports = ${JSON.stringify(
      config,
      null,
      2
    )};`;
    await fs.writeFile(tempConfigPath, configContent, "utf-8");

    // Comando para executar o Unlighthouse
    const command = `npx unlighthouse-ci \
      --config-file ${tempConfigPath} \
      --urls / \
      --reporter json \
      --output-path ${baseOutputDir}`;

    console.log(`Executando comando: ${command}`);

    // Executa o comando
    const { stdout, stderr } = await execPromise(command);

    if (stdout) console.log("Saída:", stdout);
    if (stderr) console.error("Erro:", stderr);

    // Lê o arquivo JSON gerado
    const fileData = await fs.readFile(jsonFilePath, "utf-8");
    const result = JSON.parse(fileData);

    // console.log("Conteúdo do JSON gerado:", result);

    if (!result || result.length === 0 || !result[0]) {
      throw new Error("O resultado do Unlighthouse está vazio ou inválido.");
    }

    // Remove o arquivo de configuração temporário
    await fs.unlink(tempConfigPath);

    // Extrai os dados da análise
    const analysis = result[0];
    const {
      score,
      performance,
      accessibility,
      "best-practices": bestPractices,
      seo,
    } = analysis;

    // Caminho do arquivo JSON gerado
    let rawReport = null;
    let relatorioTraduzido = null;
    try {
      const jsonReportPath = path.join(
        baseOutputDir,
        "reports",
        "lighthouse.json"
      );

      // Lê o relatório bruto
      rawReport = JSON.parse(await fs.readFile(jsonReportPath, "utf-8"));

      // // Traduz o relatório bruto para o português
      // try {
      //   relatorioTraduzido = await translate(rawReport, "pt", "en");
      //   console.log("Relatório traduzido:", relatorioTraduzido);
      // } catch (err) {
      //   console.error("Erro ao traduzir o JSON:", err);
      //   relatorioTraduzido = null;
      // }
    } catch (err) {
      console.error("Erro ao ler o relatório bruto:", err);
      rawReport = null; // Define como nulo em caso de erro
    }
    
    // Salvar no banco de dados utilizando a função modularizada
    const savedAnalysis = await saveAnalysisToDB({
      siteUrl,
      score,
      performance,
      accessibility,
      bestPractices,
      seo,
      rawReport, // Relatório bruto
      relatorioTraduzido, // Relatório traduzido
    });

    return res.status(200).json({
      message: "Relatório gerado e salvo com sucesso",
      data: savedAnalysis,
    });
  } catch (error) {
    console.error("Erro:", error);
    return res.status(500).json({
      error: "Falha ao processar o relatório",
      details: error.message,
    });
  }
}
