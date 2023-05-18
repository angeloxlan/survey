document.addEventListener('alpine:init', () => {
    Alpine.data('clipboard', () => ({
        isCopied: false,
        copyToClipboard() {
            const url = this.$refs['url'].textContent;
            navigator.clipboard.writeText(url)
                .then(() => {
                    this.isCopied = true;
                    setTimeout(() => {
                        this.isCopied = false;
                    }, 2500);
                });
        },
    }))
})
