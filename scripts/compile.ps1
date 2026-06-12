# Compile stub LaTeX → output/final.pdf (LuaLaTeX + biber, ~4 passes)
$ErrorActionPreference = "Stop"
$Root = Split-Path $PSScriptRoot -Parent
$LatexDir = Join-Path $Root "output\latex"
$Template = Join-Path $Root "templates\main.tex"
$FinalPdf = Join-Path $Root "output\final.pdf"

Copy-Item $Template (Join-Path $LatexDir "main.tex") -Force

Push-Location $LatexDir
try {
    foreach ($i in 1..2) {
        Write-Host "lualatex pass $i..."
        & lualatex -interaction=nonstopmode -halt-on-error main.tex
        if ($LASTEXITCODE -ne 0) { throw "lualatex failed on pass $i" }
    }
    Write-Host "biber..."
    & biber main
    if ($LASTEXITCODE -ne 0) { throw "biber failed" }
    foreach ($i in 3..4) {
        Write-Host "lualatex pass $i..."
        & lualatex -interaction=nonstopmode -halt-on-error main.tex
        if ($LASTEXITCODE -ne 0) { throw "lualatex failed on pass $i" }
    }
    Copy-Item (Join-Path $LatexDir "main.pdf") $FinalPdf -Force
    Write-Host "Wrote $FinalPdf"
}
finally {
    Pop-Location
}
