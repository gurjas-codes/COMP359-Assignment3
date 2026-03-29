import time

def print_header(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def main():
    print_header("LINEAR PROGRAMMING SIMPLEX VISUALIZATION")
    print("Running all components...")
    
    start_time = time.time()
    
    
    elapsed = time.time() - start_time
    print_header(f"COMPLETE - Elapsed time: {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()