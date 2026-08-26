# JOCKY Forensics Console

Create a simple one-page frontend prototype for a project called "JOCKY".



IMPORTANT:

This is ONLY a visual frontend prototype.



Do NOT create a backend.

Do NOT create a database.

Do NOT create authentication.

Do NOT create API integrations yet.

Do NOT create multiple pages.

Do NOT install unnecessary libraries.



Keep the implementation small and simple so the project remains easy to edit later.



PROJECT:



JOCKY is a digital forensics command-line tool with a graphical interface.



The prototype should allow a user to:

1. Enter a forensic command.

2. Click an Execute button.

3. See a sample result.

4. See a small list of recent commands.



DESIGN:



Create a clean, modern and presentable dark-themed interface.



Use:

- dark charcoal background

- blue/cyan accent

- white/light-gray text

- subtle borders

- rounded cards

- clean typography

- simple hover effects

- generous spacing



Avoid:

- excessive neon

- Matrix effects

- hacker clichés

- skulls

- excessive animations

- complicated enterprise dashboard styling



The goal is a good-looking student/hackathon prototype.



LAYOUT:



ONE PAGE ONLY.



TOP NAVBAR:



Left:

JOCKY



Small subtitle:

Digital Forensics Tool



Right:

● API Connected



MAIN CONTENT:



Heading:

Digital Forensics Command Center



Description:

"Analyze digital evidence using simple JOCKY forensic commands."



COMMAND CARD:



Title:

Command Center



Label:

Enter JOCKY Command



Create a large text input.



Placeholder:

HASH FILE evidence.txt



Create a button:

Execute Command



Below it show:



Examples:

HASH FILE evidence.txt

SYSTEM INFO

LIST FILES



RESULT CARD:



Title:

Execution Result



Initially show:

"No command executed yet."



When the user clicks Execute Command, display a MOCK result.



Example:



Status: Success



Command:

HASH FILE evidence.txt



Result:

SHA-256: a3f5c91d8b7e...



Clearly treat this as mock/demo output.



RECENT COMMANDS:



Create a small section titled:

Recent Commands



Show:



HASH FILE evidence.txt     Success

SYSTEM INFO                Success

LIST FILES                 Success



Keep this section compact.



IMPORTANT:

The Execute button only needs to show mock data for now.



Do not connect it to a backend yet.



Do not add any API code yet.



Do not add extra features.



Focus only on making this single page visually clean, responsive and presentable.



Before finishing, make sure the generated application runs correctly.

This project was built with [Lovable](https://lovable.dev).

## Build with Lovable

Continue developing this project in the [Lovable editor](https://lovable.dev/projects/636f07d7-bc97-46c6-a037-60ebfb89461e).

- **Ship faster**: describe what you want to build and Lovable handles the code.
- **Stay in sync**: every change made in Lovable is committed straight to this repository.
- **Full ownership**: this code is yours. Push to `main` on GitHub and your changes sync back into Lovable, ready for your next prompt.

## Development

Prefer working locally? You need Node.js and npm — [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating).

```sh
git clone <this-repository-url>
cd <repository-name>
npm i
npm run dev
```
