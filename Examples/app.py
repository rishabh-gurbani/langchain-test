from flask_cors import CORS
import os
from flask import Flask, request, jsonify
import replicate
import openai
os.environ["OPENAI_API_KEY"] = "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"
os.environ["REPLICATE_API_TOKEN"] = "r8_YFEWnVF5TfFYluwd0g1Mq6x7mVhuH6l1abPLc"

app = Flask(__name__)
CORS(app)

@app.route('/get_response', methods=['POST'])
def get_response():
    message = request.json.get('message')
    print(message)

    if message:
        outfit_messages = [
            {"role": "system",
             "content": """
             you are a fashion expert and have a unique sense of design understanding modern trends.
             give 1 detailed outfit suggestions for :
            outfit
            for each one suggest appropriate footwear accessories.

            give output like this:
            Sure here's your outfit suggestion
            Title : Traditional Elegance
            Outfit: Emerald green silk saree with subtle gold embroidery, paired with a matching embellished blouse.
            Footwear: Gold-toned embellished juttis.
            Accessories: Delicate gold necklace, thin bangles, small pearl studs, and a simple emerald green potli bag.

            describe only the outfits, dont type anything else like sure here are outfits"""},
        ]

        image_prompts = [
            {"role": "system",
             "content": """
                     Craft fashion image descriptions for user input, enhancing appeal. Given attire details, generate aesthetic vivid model and setting depiction in 100 words, boosting allure for potential buyers.

                example input : Outfit: Peach-colored lehenga choli with floral embroidery, paired with a matching net dupatta.
                 Footwear: Beige embroidered mojris.
                Accessories: Pearl drop earrings, a delicate gold waist belt, and a peach-colored potli bag with gold accents.

                example output : Elegance personified, our model graces the scene in a resplendent peach-hued lehenga choli, a canvas of delicate floral embroidery that tells a story of craftsmanship. 
                The matching net dupatta drapes like a whisper, adding an ethereal touch. Her feet adorned with beige embroidered mojris, each step is a dance of comfort and style. 
                The ensemble is not complete without the pearl drop earrings, their luster echoing her grace. A delicate gold waist belt cinches the look, a gleaming homage to tradition. To hold secrets and dreams, 
                she carries a peach potli bag, its gold accents glinting like the promises of a magical evening.

                input : {input}
                output :"""},
        ]

        if message:
            outfit_messages.append(
                {"role": "user", "content": message},
            )
            outfit_recc = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=outfit_messages
            )
            outfit_messages.append(
                {"role" : "assistant", "content": outfit_recc.choices[0].message.content}
            )

            image_prompts.append(
                {"role": "user", "content": outfit_recc.choices[0].message.content},
            )
            image_prompt = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=image_prompts
            )

        reply = outfit_recc.choices[0].message.content
        print(f"ChatGPT\n: {reply}")

        image = image_prompt.choices[0].message.content

        output = replicate.run(
            "stability-ai/sdxl:a00d0b7dcbb9c3fbb34ba87d2d5b46c56969c84a628bf778a7fdaec30b1b99c5",
            input={"prompt": image}
        )

        output_image_url = output[0]
        print(output_image_url)

        return jsonify({"idea": reply, "image": output_image_url})

    return jsonify({"error": "Missing 'message' in form data."})


if __name__ == "__main__":
    app.run(debug=True)


