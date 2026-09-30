param(
    [Parameter(Mandatory=$true)]
    [string]$PptxPath,
    [string]$OutputDir = ""
)

if (-not (Test-Path $PptxPath)) {
    Write-Error "File not found: $PptxPath"
    exit 1
}

$resolvedPptx = (Resolve-Path $PptxPath).Path
if ($OutputDir -eq "") {
    $OutputDir = Split-Path -Parent $resolvedPptx
}

if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

$baseName = [System.IO.Path]::GetFileNameWithoutExtension($resolvedPptx)

$ppt = New-Object -ComObject PowerPoint.Application
try {
    # Open presentation hidden, read-only
    $pres = $ppt.Presentations.Open($resolvedPptx, 1, 0, 0)
    $slideCount = $pres.Slides.Count

    for ($i = 1; $i -le $slideCount; $i++) {
        $outImg = Join-Path $OutputDir ("${baseName}_slide_${i}.png")
        $pres.Slides.Item($i).Export($outImg, "PNG", 1920, 1080)
        Write-Host "Exported Slide $i -> $outImg"
    }

    $pres.Close()
}
finally {
    $ppt.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($pres) | Out-Null
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}

Write-Host "Rendered $slideCount slides successfully."
