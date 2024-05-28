$ollamaProc = Start-Process "C:\Users\Eitan Baron\AppData\Local\Programs\Ollama\ollama app.exe" -ArgumentList "serve" -NoNewWindow -PassThru
Write-Host "True"
if ($null -ne $ollamaProc) {
    return $true
}else{
    return $false
}