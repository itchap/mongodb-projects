export function sendChatMessage(question) {
    const productId = $('#product-details').data('product-id');
    $('#chat-messages').append(`<div class="message-bubble user-message"><strong>You:</strong> ${escapeHtml(question)}</div>`);
    scrollToLatestMessage();
    showLoadingIndicator(true);
    $.ajax({
        url: `/fashionbot`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ product_id: productId, question: question }),
        success: function (response) {
            const formattedAnswer = formatChatMessage(response.answer);
            $('#chat-messages').append(`<div class="message-bubble bot-message"><strong>FashionBot:</strong> ${formattedAnswer}</div>`);
            displayChatRecommendations(response.recommendations);
            showLoadingIndicator(false);
            scrollToLatestMessage();
        },
        error: function (xhr, status, error) {
            showLoadingIndicator(false);
            const message = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : 'An unexpected error occurred. Please try again later.';
            showError(message);
            $('#chat-messages').append('<div class="message-bubble bot-message"><strong>FashionBot:</strong> Sorry, something went wrong. Please try again later.</div>');
            scrollToLatestMessage();
        }
    });
}

function scrollToLatestMessage() {
    const chatContainer = $('#chat-messages');
    chatContainer.scrollTop(chatContainer.prop("scrollHeight"));
}

function escapeHtml(text) {
    return text.replace(/[&<>"'\/]/g, function (s) {
        return entityMap[s];
    });
}

function formatChatMessage(text) {
    // Replace newlines with <br>
    text = text.replace(/\n/g, '<br>');
    
    // Handle markdown-like list items
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>'); // Bold text
    text = text.replace(/1\.\s(.*?)\n/g, '<li>$1</li>'); // List items starting with numbers
    
    // Wrap list items with <ul> tag
    text = '<ul>' + text + '</ul>';
    
    return text;
}

function displayChatRecommendations(recommendations) {
    $('#chat-recommendations').empty();
    recommendations.forEach(function (item) {
        $('#chat-recommendations').append(`
            <img src="${item.images[0]}" class="thumbnail-product" alt="${item.name}" data-id="${item._id}">
        `);
    });
}

function showLoadingIndicator(show) {
    if (show) {
        $('.loading-indicator').show();
    } else {
        $('.loading-indicator').hide();
    }
}

function showError(message) {
    $('#error-message').text(message).show();
    setTimeout(function () {
        $('#error-message').hide();
    }, 5000);
}

// Entity map for escaping HTML
const entityMap = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
    '/': '&#x2F;',
};