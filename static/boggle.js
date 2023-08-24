// Boggle Class
class BoggleGame {
    // Make a Game at Current DOM ID
    constructor(boardID, secs=60) {
        this.secs = secs;
        this.showTimer();

        this.score = 0;
        this.words = new Set()
        this.board = $("#" + boardID)

        this.timer = setInterval(this.tick.bind(this), 1000)

        $(".add-word", this.board).on('submit', this.handleSubmit.bind(this));
    }

    // Show word in list of words
    showWord(word) {
        $(".words", this.board).append($("<li>", {text: word}));
    }

    // Show score in html
    showScore() {
        $('.score', this.board).text(this.score)
    }

    // Show a Status Message
    showMessage(msg, cls) {
        $('.msg', this.board).text(msg).removeClass().addClass(`msg ${cls}`);
    }

    // Handle submission of word: if unique and valid, score and show
    async handleSubmit(evt) {
        evt.preventDefault();
        const $word = $(".word", this.board);

        let word = $word.val();
        if (!word) return;

        if (this.words.has(word)) {
            this.showMessage(`Already found ${word}`, "err");
            return;
        }

        // check server for validity
        const resp = await axios.get("/check-word", { params: { word: word }});
        if (resp.data.result === "not-word") {
            this.showMessage(`${word} is not a valid English word`, "err");
        } else if (resp.data.result === "not-on-board") {
            this.showMessage(`${word} is not a valid word on this board`, "err");
        } else {
            this.showWord(word);
            this.score += word.length;
            this.showScore();
            this.words.add(word);
            this.showMessage(`Added: ${word}`, "ok");
        }

        $word.val("").focus();

    }

    // Update Timer in DOM
    showTimer() {
        $('.timer', this.board).text(this.secs)
    }

    // Tick: handle a second passing in game
    async tick() {
        this.secs -= 1
        this.showTimer()

        if(this.secs === 0) {
            clearInterval(this.timer);
            await this.scoreGame();
        }
    }

    // End of Game: Score and Update Message
    async scoreGame() {
        $('.add-word', this.board).hide();
        const resp = await axios.post("/post-score", { score: this.score });
        if(resp.data.brokeRecord) {
            this.showMessage(`New Record: ${this.score}`, "ok")
        } else {
            this.showMessage(`Final Score: ${this.score}`, "ok")
        }
    }
}