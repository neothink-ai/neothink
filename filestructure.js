const fs = require("fs");
const path = require("path");

function listFiles(dir, depth = 0) {
  const files = fs.readdirSync(dir);
  files.forEach((file) => {
    const fullPath = path.join(dir, file);
    const stats = fs.statSync(fullPath);
    const prefix = " ".repeat(depth * 2);
    console.log(prefix + file);
    if (stats.isDirectory()) {
      listFiles(fullPath, depth + 1); // Recurse into directories
    }
  });
}

const directoryPath =
  "e:/Smruie In Uni/PAPERS AND PROJECTS\3 Sem - ELNeothink\neothink"; // Replace with your folder path
listFiles(directoryPath);
