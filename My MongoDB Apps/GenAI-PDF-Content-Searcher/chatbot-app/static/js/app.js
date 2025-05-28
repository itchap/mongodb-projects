$(document).ready(function() {
    // PDF upload form submission handler
    $("#uploadForm").on("submit", function(e) {
        e.preventDefault(); // Prevent the default form submission

        let formData = new FormData();
        let file = $("#pdf-file")[0].files[0];
        formData.append("file", file);

        // Show the loading message and disable the button
        $("#loading-message").show();
        $("#uploadForm button").prop("disabled", true);

        // Send the PDF to the Flask backend
        $.ajax({
            url: "/upload",
            type: "POST",
            data: formData,
            processData: false,  // Tell jQuery not to process the data
            contentType: false,  // Tell jQuery not to set the content type header
            success: function(response) {
                alert("PDF uploaded and processed successfully!");
                // Hide the loading message and reset form
                $("#loading-message").hide();
                $("#uploadForm button").prop("disabled", false);
                $("#file-name").text(''); // Clear the file name
                // Optional: Trigger a page refresh to clear everything
                location.reload(); // Reload the page to prevent re-uploading
            },
            error: function(xhr, status, error) {
                alert("Error uploading or processing the PDF: " + error);
                // Hide the loading message and enable the button again
                $("#loading-message").hide();
                $("#uploadForm button").prop("disabled", false);
            }
        });
    });

    // Update the selected file name when a file is chosen
    $("#pdf-file").on("change", function() {
        let fileName = $(this).val().split("\\").pop();  // Extract the file name
        $("#file-name").text(fileName);  // Display the file name next to the upload form
    });

    // Existing chat request functionality
    $("#submit-btn").on("click", function() {
        let question = $("#question-input").val().trim(); // Get user input
        if (question) {
            addMessageToChat("user", question);  // Add the user's question to the chat log
            $("#question-input").val("");        // Clear the input field after the question is submitted
            sendQuestionToAPI(question);         // Send the user's question to the API
        }
    });

    // Function to add messages (user or bot) to the chat log
    function addMessageToChat(sender, message, isMarkdown = false) {
        let chatLog = $("#chat-log");  // Select the chat log container
        let messageHtml;

        // Convert markdown to HTML if applicable
        if (isMarkdown) {
            messageHtml = `<div class="chat-message ${sender}">${marked.parse(message)}</div>`;
        } else {
            messageHtml = `<div class="chat-message ${sender}">${message}</div>`;
        }

        chatLog.append(messageHtml);                 // Append the message to the chat log
        chatLog.scrollTop(chatLog[0].scrollHeight);  // Scroll to the bottom of the chat log
    }

    // Send the user's question to the Flask backend API via AJAX
    function sendQuestionToAPI(question) {
        $.ajax({
            url: "/ask",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ question: question }),
            success: function(response) {
                let answer = response.answer;       // Extract the bot's answer
                addMessageToChat("bot", answer, true);  // Display the bot's answer (with markdown)
            },
            error: function(xhr, status, error) {
                addMessageToChat("bot", "Error: Unable to get a response at the moment.");  // Show an error message in the chat log
            }
        });
    }

    // Allow pressing 'Enter' to submit the question
    $("#question-input").keypress(function(e) {
        if (e.which === 13) {  // Check if the 'Enter' key was pressed
            $("#submit-btn").click();  // Trigger the 'Ask' button click event
        }
    });
});