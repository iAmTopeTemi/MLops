package org.example

class SecurityScan {
    def scan(String modelPath) {
        def script = libraryResource 'org/example/SecurityScanScript.sh'
        def tempScript = 'tempSecurityScanScript.sh'
        writeFile file: tempScript, text: script
        sh "chmod +x ${tempScript}"
        sh "./${tempScript} ${modelPath}"
    }
}
