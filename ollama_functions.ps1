function Start-Ollama {
    Start-Process "C:\Users\Eitan Baron\AppData\Local\Programs\Ollama\ollama app.exe" -ArgumentList "serve" -NoNewWindow -PassThru
}

function Check-OllamaResponsive {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:11434/ping" -TimeoutSec 10
        if ($response.StatusCode -eq 200) {            
            return $true
        } else {            
            return $false
        }
    } catch {        
        if ($_.Exception.Response.StatusCode -eq 404) {            
            return $true
        } else {
            return $false
        }
    }
}

function Restart-Ollama {
    $ollamaProc = Get-Process -Name "C:\Users\Eitan Baron\AppData\Local\Programs\Ollama\ollama app.exe" -ErrorAction SilentlyContinue
    if ($null -ne $ollamaProc) {
        Write-Host "Killing Ollama process: $($ollamaProc.Id)"
        $ollamaProc | Stop-Process -Force
        Start-Sleep -Seconds 15
    } else {
        Write-Host "No Ollama process found."
    }   
    Start-Ollama 
}