# Sequential Queries (with nanosecond precision)
start_time=$(date +%s%N)

# Sequential query execution
dig @127.0.0.1 -p 5354 google.com
dig @127.0.0.1 -p 5354 yahoo.com
dig @127.0.0.1 -p 5354 example.com

# End time in nanoseconds
end_time=$(date +%s%N)

# Calculate elapsed time in nanoseconds
elapsed_time=$((end_time - start_time))

# Convert elapsed time to seconds
elapsed_time_seconds=$(echo "scale=3; $elapsed_time / 1000000000" | bc)

echo "Total time for sequential queries: $elapsed_time_seconds seconds"

# Parallel Queries (with nanosecond precision)
start_time=$(date +%s%N)

# Parallel query execution
echo -e "google.com\nyahoo.com\nexample.com" | xargs -I {} -P 3 dig @127.0.0.1 -p 5354 {}

# End time in nanoseconds
end_time=$(date +%s%N)

# Calculate elapsed time in nanoseconds
elapsed_time=$((end_time - start_time))

# Convert elapsed time to seconds
elapsed_time_seconds=$(echo "scale=3; $elapsed_time / 1000000000" | bc)

echo "Total time for parallel queries: $elapsed_time_seconds seconds"
