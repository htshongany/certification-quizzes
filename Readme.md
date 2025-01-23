# Quiz Repository

Welcome to my GitHub repository dedicated to certification quizzes! Here, you'll find JSON files with quizzes to help you review and practice for online exams.

## Quiz Format

All quizzes should follow the JSON format outlined here: [json file](quiz-json/model.json)

### Format Details:

- **`question`**: The question being asked.
- **`options`**: A list of possible answer choices.
- **`answer`**: The index (or indices) of the correct answer(s) within the **`options`** list (note: indexing starts at `0`).

### Supported Question Types:

1. **Single-answer questions** (one correct choice).  
2. **Multiple-answer questions** (more than one correct choice).  

## How to Contribute

1. **Add quizzes**: Submit your own quizzes in JSON format via a pull request.
2. **Share files**: We encourage the community to share their JSON quiz files to expand the repository.
3. **Test with the app**: Use the simple HTML/JS application to simulate your quizzes. [Launch the app](https://htshongany.github.io/certification-quizzes/quiz-app/index.html)

## Credit

- The **Cloud-Practitioner-exam** quiz is based on the [AWS Certified Cloud Practitioner Notes](https://github.com/kananinirav/AWS-Certified-Cloud-Practitioner-Notes).