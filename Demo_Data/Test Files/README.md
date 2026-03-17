# Test Files Directory

## 4SICSGeekLounge151.pcap

This directory should contain the **4SICS ICS Lab PCAP file** for testing the PCAP analysis feature.

### File Details
- **Name**: `4SICSGeekLounge151.pcap`
- **Size**: ~25 MB
- **Source**: 4SICS ICS Lab CTF
- **Content**: Real ICS/SCADA network traffic

### How to Add the File

1. Download from the official source or use your verified copy
2. Place the file in this directory: `Test Files/Test Files/4SICSGeekLounge151.pcap`
3. Verify the file is valid:
   ```bash
   file "Test Files/Test Files/4SICSGeekLounge151.pcap"
   # Should show: "tcpdump capture file" or similar
   ```

### Usage

Once the file is in place, analyze it with:

```bash
python -m cli.main analyze-pcap "Test Files/Test Files/4SICSGeekLounge151.pcap" -o 4sics_report.html --format html
```

### Note

The current placeholder file is empty (0 bytes). Please replace it with the actual 25MB PCAP file.
