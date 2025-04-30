1. Your completed code with:

Working implementation => I have implemented a working prototype. I have attached the code to my email.

Documentation of your approach => I first load my model/prompt configurations stored in a yaml/json file. I then store them in global variables.
I use LLaMA 3.2 3B model because it is a very good text generation language model and it is available for free on HuggingFace.
Firstly, I validate the email data input for each id. Then I classify the email using LLaMA, then I generate a response based on the email and 
the classification. I use appropriate error handling for each email classification and generation. 

Examples run =>

Email 1: Subject: Re: Damaged Product Received - Complaint Response
Dear [Customer's Name],
Thank you for bringing this issue to our attention. We apologize for the unacceptable condition of your order, which is completely unacceptable and not up to our quality standards. We have created an urgent ticket to address this matter and ensure a prompt resolution.
Please expect a refund for the damaged product, as well as any additional compensation for the inconvenience caused. Our dedicated team will review the situation and provide a full refund within the next 48 hours.
Your satisfaction is our top priority, and we appreciate your feedback. We will use this as an opportunity to review our packaging and shipping procedures to prevent such incidents in the future.
Thank you for your patience and understanding.
Best regards,
[Your Name]

Email 2: Subject: Re: Question about product specifications
Dear [Customer],
Thank you for your interest in our premium package. I'm happy to help clarify the compatibility of our product with Mac OS. Our premium package is compatible with Mac OS, and we provide detailed specifications on our website. However, I'd be more than happy to provide you with the specific details you're looking for.
Please find the specifications here: [link to product specifications]. If you have any further questions or concerns, feel free to ask.
Best regards,
[Your Name]

Email 3: Subject: Re: Amazing customer support
Dear [Customer],
Thank you so much for your kind words about your recent interaction with Sarah on our team! We're thrilled to hear that she was able to provide you with excellent support and resolve your issue to your satisfaction. We're proud of our team for going above and beyond to ensure our customers receive the best possible service.
We appreciate your feedback and will continue to strive for excellence in all our interactions.
Best regards,
[Your Name]

Email 4: Subject: Re: Support Request - Error Code 5123
Dear [Customer Name],
Thank you for reaching out to us for assistance. I'm happy to help you resolve the issue with the software installation. I've created a support ticket for you, and I'll be happy to guide you through the troubleshooting process.
Can you please try updating the software to the latest version and then try reinstalling it? If the issue persists, we can explore further solutions together.
I'll be in touch with you soon to discuss the next steps.
Best regards,
[Your Name]

Email 5: Subject: Re: Partnership Opportunity
Dear [Customer Name],
Thank you for your email expressing interest in a potential partnership opportunity with our company. We're excited to explore possibilities and would be delighted to schedule a call to discuss this further.
How about we schedule a call for Wednesday, [Date], at 2 PM EST or Thursday, [Date], at 10 AM EST? Please let us know which time slot works best for you, or suggest an alternative time that suits you.
We're looking forward to speaking with you and exploring ways we can collaborate.
Best regards,
[Your Name]


2. Documentation of your prompt iterations, including:

Initial prompts => I have added all my prompts in a json file that I have attached in the email.

Problems encountered and Improvements made => The first problem was with the email generation. My model was not scheduling a day/time for a metting when requested by
the user. I fixed it, but the next problem occurred. My model started scheduling meetings for all email categories, even for feedback ones.
So, my next prompt fixed that but it did not handle edge cases like creating tickets. I added that in my final prompt.

3. A brief summary covering:

Your design decisions => I used LLaMA because it is open-source and the 3.2 version performs well for text generation tasks.
I used the 3B parameter model instead of 8B, because 3B is a good amount of parameters to process the email efficiently.

Challenges encountered => LLaMA returns the entire prompt in the results, so I had to extract the actual output from LLaMA's response.
Another challenge was GPU constraints. So I had to use a quantized model for LLaMA and I had to use Gooogle Colab to run the model.

Potential improvements => I would consider using a better model given resources like GPT-4o. Other improvements would be to
collect more data and define more categories instead of just 5.

Production considerations => A ticket system can be implemented easily. We should connect our model to the database.
That way we can actually connect the customers with our staff and add their names/availability in the email. We can also connect
our AI agent to a calendar to check for staff availablity and schedule meetings accordingly. We also need to implement
security measures to prevent our server from crashing against DDOS attacks.