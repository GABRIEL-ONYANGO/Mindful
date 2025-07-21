from flask import Flask, render_template, request, jsonify
import os
import speech_recognition as sr
from gtts import gTTS
import pyttsx3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        said = " "

        try:
            said = r.recognize_google(audio)
            print("You:", said)
        except Exception as e:
            print("Exception: " + str(e))

    return said

def print_conversation(user_input, assistant_response):
    print("You said:", user_input)
    print("Annie:", assistant_response)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_input', methods=['POST'])
def process_input_route():
    data = request.json
    user_input = data.get('inputText')

    if user_input == "voice_input":
        user_input = get_audio()
        print("User's Voice Input:", user_input)
    
    bot_response = process_input(user_input)
    generate_audio_response(bot_response)
    
    return jsonify({"response": bot_response})

def generate_audio_response(text):
    tts = gTTS(text)
    tts.save("response.mp3")
    os.system("mpg321 response.mp3")

def process_input(user_input):
    user_input = user_input.lower()

    if "hello" in user_input:
        return "Hello, how are you today?"

    elif "hi" in user_input:
        return "Hi, how are you today?"

    elif "hey" in user_input:
        return "Hey there, how are you today?"

    elif "what is your name" in user_input:
        return "My name is Annie. I'm your online therapist. What is your name?"

    elif "my name is" in user_input:
        name = user_input.split("my name is")[-1].strip()
        return f"Nice to meet you, {name}. How can I assist you?"
    
    elif "i have been feeling depressed a lot lately" in user_input:
        return "I am sorry to hear that, Depression is a common and serious mood disorder that affects how you feel, think, and handle daily activities. It goes beyond the temporary feelings of sadness that everyone experiences from time to time. Please tell me how you've been feeling"

    elif "it's hard to get out of bed, and I don't enjoy doing things I used to love anymore." in user_input:
        return "It sounds like you've been experiencing a loss of interest and low mood, which are common symptoms of depression. I want you to know that you're not alone, and I'm here to support you. Can you tell me a bit more about other things you've been going through?"
    
    elif "i don't really know how to explain it. It's like this heavy cloud is hanging over me" in user_input:
        return "It sounds like depression has been weighing you down.Do you feel like it's affecting your relationships in any way?"

    elif "yes, it's draining all my energy. I've been isolating myself from friends and family." in user_input:
        return "Remember that depression is an illness, and it's not your fault."
    
    elif "it's just hard to see any hope or joy in anything." in user_input:
        return "How have your relationships been impacted by your feelings of being a burden?"

    elif "i feel like I'm constantly bringing everyone down with my problems." in user_input:
        return "It's understandable that you may feel that way, but it's important to remember that your loved ones care about you and want to support you"
    
    elif "i don't want to burden them with my issues, so I keep everything to myself." in user_input:
        return "Sharing your feelings and allowing them to help can strengthen your relationships."

    elif "it's getting harder to keep pretending that everything is okay." in user_input:
        return "Depression can make it challenging to see things clearly, so let's work together to find healthier ways to cope and communicate with your support system. How have you been taking care of yourself during this difficult time?"
    
    elif "honestly, I haven't been taking care of myself at all." in user_input:
        return "When depression takes hold, it can be challenging to engage in self-care. However, taking care of yourself is crucial for your well-being."

    elif "i've lost my appetite and my sleep patterns are messed up" in user_input:
        return "We can start by setting small, achievable goals for self-care. For example, establishing a regular sleep routine and ensuring you have a balanced diet can have a positive impact on your mood. We'll work together to find strategies that work best for you."
    
    elif "it's like I've lost all motivation." in user_input:
        return "What are some activities or hobbies that used to bring you joy?"
    
    elif "i used to enjoy painting and playing the guitar, but I haven't touched them in months." in user_input:
        return "It's not uncommon for depression to dampen your interests and passions. Although it may feel difficult right now, engaging in activities that you once enjoyed can help alleviate depressive symptoms."
    
    elif "it feels like I've lost interest in everything." in user_input:
        return "Let's start by reintroducing those activities gradually. Start with short sessions and see how it feels. Remember, the goal is not to feel an immediate sense of joy but to gradually regain a sense of pleasure and accomplishment. We'll work on finding the right balance for you. In addition to therapy, have you considered any other forms of support, such as medication or a support group?"
    
    elif "i haven't thought about medication yet, but I'm open to exploring it if it could help." in user_input:
        return "It's great that you're open to considering medication as an option. I would recommend speaking with a psychiatrist who can evaluate your symptoms and determine if medication might be beneficial in your case. They can provide you with the necessary information and guidance to make an informed decision. What about a support group?"
    
    elif "as for support groups, I'm not sure. I worry that talking to others who are also struggling might make me feel worse." in user_input:
        return "Regarding support groups, I understand your concerns. It's essential to find the right support group that aligns with your needs and preferences. There are various types of groups, and some focus on sharing experiences, providing empathy, and learning coping strategies. Participating in a support group can help you realize that you're not alone in your struggles and provide a safe space for discussing your feelings. However, it's entirely up to you whether you feel ready for that step. We can explore other avenues of support as well.In the meantime, I'd like to help you develop some coping mechanisms to manage your depression symptoms. Have you tried any relaxation techniques or mindfulness exercises before?"
    
    elif "no, I haven't really tried anything like that before." in user_input:
        return "Mindfulness exercises and relaxation techniques can be helpful in reducing stress and improving your overall well-being. Let's start with a simple breathing exercise. Take a deep breath in, hold it for a few seconds, and then exhale slowly. Try to focus your attention on your breath as you repeat this process a few times. It's normal for your mind to wander, but gently bring your focus back to your breath each time. We can explore more techniques like progressive muscle relaxation or guided imagery in future sessions. Remember, therapy is a collaborative process, and we'll work together to find the strategies that work best for you. Is there anything else you'd like to discuss today, or any specific goals you have for our sessions?"
    
    elif "what goals? I don't have any goals." in user_input:
        return "Of course, let's discuss your goals for our sessions. It's important to have a clear direction and focus on what you would like to achieve. What would you like to work on or change in your life?"
    
    elif "exit" in user_input or "bye" in user_input:
        return "Goodbye!"

    else:
        return "I'm sorry, I didn't understand that. Can you please repeat?"

    pass

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
