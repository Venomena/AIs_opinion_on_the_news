#!/bin/bash

echo "Starting the Flask application..."

# Define cleanup function
function clean_up {
    echo "Stopping Flask app..."
    kill $FLASK_PID
    echo "Flask app stopped."
    echo "Script terminated."
    exit 0
}

# Set the FLASK_APP environment variable
export FLASK_APP=app.py
export FLASK_ENV=development

# Start the Flask application in the background on port 5004
flask run --host=0.0.0.0 --port=5004 & 
FLASK_PID=$!
echo "Flask app started on port 5004."

# Ensure the cleanup function is called on script exit
trap clean_up SIGINT SIGTERM

echo "Entering loop to generate new blog posts periodically..."
# Initialize the firstRun flag to true
firstRun=true
# Start the loop to generate new blog posts periodically
while true; do
    echo "Current time: $(date)"
    # If it's not the first run, generate a summary before the next post
    if [ "$firstRun" = false ]; then
        echo "Generating summary of all blog posts..."
        python3 generate_sum.py
        if [[ $? -eq 0 ]]; then
            echo "Summary generated successfully."
        else
            echo "Failed to generate summary."
        fi
    else
        firstRun=false
    fi

    echo "Generating new blog post..."
    python3 generate_blog.py
    if [[ $? -eq 0 ]]; then
        echo "Blog post generated successfully."
    else
        echo "Failed to generate blog post."
    fi
    # Calculate the next time for a blog post generation, waiting for 6 hours
    echo "Next blog post will be generated after 5 sec."
    sleep 21600  # Adjusted for testing; originally planned for 6 hours
done