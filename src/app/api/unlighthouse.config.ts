module.exports = (siteUrl: any, device: any) => {
  return {
    ci: {
      reporter: "json", // Remova os colchetes e passe como string simples
      outputPath: "./reports", // Agora é um diretório
    },
    site: siteUrl, // URL do site recebida dinamicamente
    debug: true, // Habilita logs de depuração
    scanner: {
      device: device === "mobile" ? "mobile" : "desktop", // Alinhar as configurações do dispositivo
    },
    includeUrls: [
      "^/$", // Apenas a página principal (índice)
    ],
  };
};

//documentação unlighthouse
// https://unlighthouse.dev/integrations/ci#build-static-report

// comando CLI para executar somente a página principal
//unlighthouse https://mscultural.ms.gov.br --config-file unlighthouse.config.ts --urls /

// comanda CI para executar somente a página principal e salvar o resultado em json
// unlighthouse-ci --config-file unlighthouse.config.ts --urls / --reporter json --output-path ./resultado.json
