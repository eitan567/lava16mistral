function Start-Ollama {
    Start-Process "C:\Users\Eitan Baron\AppData\Local\Programs\Ollama\ollama.exe" -ArgumentList "serve" -NoNewWindow -PassThru
    Write-Host "Ollama service started."
}

function Check-OllamaResponsive {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:11434/ping" -TimeoutSec 10
        return $true
    } catch {
        return $false
    }
}

while ($true) {
    Write-Host "Checking if Ollama is responsive..."
    if (Check-OllamaResponsive) {
        Write-Host "Ollama is responsive."
    } else {
        Write-Host "Ollama is not responsive. Attempting to restart..."
        $ollamaProc = Get-Process -Name "ollama" -ErrorAction SilentlyContinue
        if ($null -ne $ollamaProc) {
            Write-Host "Killing Ollama process: $($ollamaProc.Id)"
            $ollamaProc | Stop-Process -Force
            Start-Sleep -Seconds 5
        } else {
            Write-Host "No Ollama process found."
        }

        Start-Ollama
    }
    Start-Sleep -Seconds 5
}
