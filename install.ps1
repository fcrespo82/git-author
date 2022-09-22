$FolderName = "$HOME/.local/bin"
if (-not (Test-Path $FolderName)) {
    New-Item $FolderName -ItemType Directory
    Write-Host "Folder $FolderName successfully"
}

new-item -Force -type SymbolicLink -Target (resolve-path ./main.py) -Path $HOME/.local/bin/git-set_author

Write-Output ""
Write-Warning "Please make sure there's a config.ini in this folder with your required profiles"
Write-Output ""
Write-Warning @"
IMPORTANT for windows users
Install Python
Disable app aliases for python in Windows 'Settings > Apps > Advanced Apps Configuration > Apps Execution Aliases'
"@