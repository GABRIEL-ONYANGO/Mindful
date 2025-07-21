const chatbotToggler = document.querySelector(".chatbot-toggler");
const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
const voiceBtn = document.querySelector(".voice-btn");

let userMessage = null; // Variable to store user's message

// Define the speak function
const speak = (text) => {
    if ('speechSynthesis' in window) {
        const synthesis = window.speechSynthesis;
        const utterance = new SpeechSynthesisUtterance(text);
        synthesis.speak(utterance);
    } else {
        console.error('Speech synthesis is not supported by this browser.');
    }
};

const createChatLi = (message, className) => {
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", `${className}`);
    let chatContent = className === "outgoing" ? `<p>${message}</p>` : `<span class="material-symbols-outlined">smart_toy</span><p>${message}</p>`;
    chatLi.innerHTML = chatContent;
    return chatLi;
}

const handleChat = (message) => {
    userMessage = message.trim();
    if (!userMessage) return;

    chatInput.value = "";
    chatbox.appendChild(createChatLi(userMessage, "outgoing"));
    chatbox.scrollTo(0, chatbox.scrollHeight);

    fetch("/process_input", {
        method: "POST",
        body: JSON.stringify({ inputText: userMessage }),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        const botResponse = data.response;
        const incomingChatLi = createChatLi(botResponse, "incoming");
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);

        // Speak the bot response
        speak(botResponse);
    })
    .catch(error => {
        console.error("Error:", error);
    });
};

const startVoiceInput = () => {
    if ("webkitSpeechRecognition" in window) {
        const recognition = new webkitSpeechRecognition(); // For Chrome
        recognition.lang = "en-US";
        recognition.start();

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            chatInput.value = transcript;
        };

        recognition.onend = () => {
            recognition.stop();
            handleChat(chatInput.value); // Handle chat after voice input
        };

        recognition.onerror = (event) => {
            console.error("Speech recognition error:", event.error);
        };
    } else {
        console.error("Speech recognition is not supported by this browser.");
    }
}

voiceBtn.addEventListener("click", () => {
    startVoiceInput();
});

sendChatBtn.addEventListener("click", () => {
    handleChat(chatInput.value);
});

closeBtn.addEventListener("click", () => {
    document.body.classList.remove("show-chatbot");
});

chatbotToggler.addEventListener("click", () => {
    document.body.classList.toggle("show-chatbot");
});
