$registryPath = "HKLM:\Software\Policies\Google\Chrome\URLAllowlist"
if (Test-Path $registryPath) {
    Remove-Item -Force $registryPath -Recurse
}

$registryPath = "HKLM:\Software\Policies\Google\Chrome\URLBlocklist"
if (Test-Path $registryPath) {
    Remove-Item -Force $registryPath -Recurse
}

$registryPath = "HKLM:\Software\Policies\Google\Chrome"
if (Test-Path $registryPath) {
    Remove-Item -Force $registryPath -Recurse
}