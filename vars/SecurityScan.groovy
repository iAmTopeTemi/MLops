def call(String modelPath) {
    echo "Starting security scan for model at ${modelPath}"
    // Load the SecurityScan class and perform the scan
    def scanner = new org.example.SecurityScan()
    scanner.scan(modelPath)
}
