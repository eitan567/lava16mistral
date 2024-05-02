function Start-Ollama {
    Start-Process "C:\Users\Eitan Baron\AppData\Local\Programs\Ollama\ollama app.exe" -ArgumentList "serve" -NoNewWindow -PassThru
    Write-Host "Ollama service started."
}

function Check-OllamaResponsive {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:11434/ping" -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-Host "Ping successful: $($response.StatusCode)"
            return $true
        } else {
            Write-Host "Ping returned unexpected status code: $($response.StatusCode)"
            return $false
        }
    } catch {
        Write-Host "Error in reaching Ollama: $_"
        if ($_.Exception.Response.StatusCode -eq 404) {
            Write-Host "Endpoint not found, but server might be up."
            return $true  # Assume server is up if only a 404 error is caught
        } else {
            return $false
        }
    }
}

while ($true) {
    Write-Host "Checking if Ollama is responsive..."
    if (Check-OllamaResponsive) {
        Write-Host "Ollama is responsive."
    } else {
        Write-Host "Ollama is not responsive. Attempting to restart..."
        $ollamaProc = Get-Process -Name "ollama app" -ErrorAction SilentlyContinue
        if ($null -ne $ollamaProc) {
            Write-Host "Killing Ollama process: $($ollamaProc.Id)"
            $ollamaProc | Stop-Process -Force
            Start-Sleep -Seconds 5
        } else {
            Write-Host "No Ollama process found."
        }

        Start-Ollama
    }
    Start-Sleep -Seconds 10
}
