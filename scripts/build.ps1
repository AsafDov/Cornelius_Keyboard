# Build Cornelious firmware on Windows through WSL.
#   .\scripts\build.ps1              build every board
#   .\scripts\build.ps1 rp2040zero   build one board
# Output: firmware\*.uf2
# Uses the WSL distro in $env:CORNELIOUS_WSL_DISTRO (default: Ubuntu).
$distro = if ($env:CORNELIOUS_WSL_DISTRO) { $env:CORNELIOUS_WSL_DISTRO } else { 'Ubuntu' }
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path -replace '\\', '/'
$wslRoot = (wsl.exe -d $distro wslpath -a $root).Trim()
wsl.exe -d $distro bash "$wslRoot/scripts/build.sh" @args
exit $LASTEXITCODE
