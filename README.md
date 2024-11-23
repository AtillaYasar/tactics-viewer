# tactics-viewer

# What's tactics?
- tactics is a product still in alpha, by Conjecture
- basically an editor and programming language (called c-tat https://tactics.dev/docs) and llm inference in one, you can use it for free via https://staging.tactics.dev/,
- (i believe that) it's part of the implementation of something they call Cognitive Emulation, which they believe is a more economically useful and safe way to implement AI, because it's less blackboxy: https://www.conjecture.dev/research/cognitive-emulation-a-naive-ai-safety-proposal

# usage
- put a tactics json in `dumpresponse.json`:
    + open dev tools -> https://tactics.dev/dashboard -> network tab -> find the `https://api.tactics.dev/getTactics?sort=%22mostRecentlyUsed%22` call -> response tab -> paste to file
- (optional) pip install colorama: https://pypi.org/project/colorama/

# screenshots

tactics overview, asking you to pick something

![cli](https://github.com/user-attachments/assets/436097c2-beed-40ee-ad73-a65f296f2dea)

after you pick something

![Screenshot_22](https://github.com/user-attachments/assets/790f4247-c2ee-47e1-b0c0-a8c70a21d46e)
