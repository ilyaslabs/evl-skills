# Makes the EVL CLI available. Prints the command to run it.
param([string]$Version = $(if ($env:EVL_VERSION) { $env:EVL_VERSION } else { "2.0.0" }))
$ErrorActionPreference = "Stop"
if (Get-Command evl -ErrorAction SilentlyContinue) { Write-Output "evl"; exit 0 }
if (-not (Get-Command java -ErrorAction SilentlyContinue)) { Write-Error "Java 17+ is required to run the EVL CLI."; exit 2 }
$dir = Join-Path $HOME ".evl"
$jar = Join-Path $dir "evl-cli-$Version-all.jar"
if (-not (Test-Path $jar)) {
  $url = "https://github.com/ilyaslabs/evl-lib/releases/download/v$Version/evl-cli-$Version-all.jar"
  [Console]::Error.WriteLine("Downloading the EVL CLI $Version from $url to $jar")
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  Invoke-WebRequest -Uri $url -OutFile "$jar.part"
  Move-Item "$jar.part" $jar
}
Write-Output "java -jar $jar"
