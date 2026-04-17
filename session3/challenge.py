import threading
import urllib.request
import os
import time

# --- Download function (runs in each thread) ---

def download_file(url, filename, results, lock):
    """
    Download a file from a URL and save it locally.

    Args:
        url:      URL to download from
        filename: local filename to save as
        results:  shared list to record outcomes
        lock:     threading.Lock for thread-safe list writes
    """
    try:
        print(f"[START] Downloading {filename}...")
        start = time.time()

        urllib.request.urlretrieve(url, filename)

        elapsed = time.time() - start
        msg = f"[DONE]  {filename} ({elapsed:.2f}s)"
        print(msg)

        with lock:
            results.append({"file": filename, "status": "success", "time": elapsed})

    except Exception as e:
        msg = f"[FAIL]  {filename} — {e}"
        print(msg)
        with lock:
            results.append({"file": filename, "status": "failed", "error": str(e)})


# --- Main program ---

if __name__ == "__main__":
    # Public domain sample files (small, fast to download)
    downloads = [
        {
            "url": "https://www.w3.org/TR/PNG/iso_8859-1.txt",
            "filename": "iso_8859.txt"
        },
        {
            "url": "https://www.ietf.org/rfc/rfc2616.txt",
            "filename": "rfc2616.txt"
        },
        {
            "url": "https://www.ietf.org/rfc/rfc791.txt",
            "filename": "rfc791.txt"
        },
        {
            "url": "https://www.w3.org/TR/xml/REC-xml-20081126.xml",
            "filename": "xml_spec.xml"
        },
    ]

    results = []
    lock = threading.Lock()
    threads = []

    print(f"Starting {len(downloads)} downloads concurrently...\n")
    total_start = time.time()

    # Create and start one thread per download
    for item in downloads:
        t = threading.Thread(
            target=download_file,
            args=(item["url"], item["filename"], results, lock)
        )
        threads.append(t)
        t.start()

    # Wait for all downloads to complete
    for t in threads:
        t.join()

    total_time = time.time() - total_start

    # --- Summary ---
    print("\n--- Download Summary ---")
    for r in results:
        if r["status"] == "success":
            print(f"  ✅ {r['file']} — {r['time']:.2f}s")
        else:
            print(f"  ❌ {r['file']} — {r['error']}")

    successful = sum(1 for r in results if r["status"] == "success")
    print(f"\n{successful}/{len(downloads)} files downloaded in {total_time:.2f}s total.")

    # --- Cleanup ---
    for item in downloads:
        if os.path.exists(item["filename"]):
            os.remove(item["filename"])
    print("Temporary files cleaned up.")