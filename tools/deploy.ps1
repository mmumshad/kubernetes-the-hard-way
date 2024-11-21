$ErrorActionPreference = 'Stop'
$vagrant = (Get-Command vagrant).Path

$currdir = (Get-Location).Path
$workdir = (Resolve-Path (Join-Path $PSScriptRoot ..\vagrant)).Path
Write-Host "Working dir: $workdir"
Push-Location $workdir

try {
    Get-ChildItem -Path (Join-Path $PSScriptRoot ..\vagrant\quick-steps) -Filter *.sh  | Sort-Object -Property Name |
    ForEach-Object {
        $name = $_.Name
        $parts = [IO.Path]::GetFileNameWithoutExtension($name) -split '-'
        for ($i = 1; $i -lt $parts.Length; $i++) {
            $target = $parts[$i]
            Write-Host -ForegroundColor Cyan  "==> vagrant ssh -c '/vagrant/quick-steps/${name}' ${target}"
            & $vagrant ssh -c "/vagrant/quick-steps/${name}" ${target}
        }
    }
}
finally {
    Pop-Location
    #[IO.Directory]::SetCurrentDirectory($currdir)
}
