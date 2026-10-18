// Detecção de idioma do navegador e persistência
(function () {
    const urlParams = new URLSearchParams(window.location.search);
    const hasLangParam = urlParams.has("lang");

    if (!hasLangParam) {
        const savedLang = localStorage.getItem("preferred_lang");
        let targetLang = "pt";

        if (savedLang) {
            targetLang = savedLang;
        } else {
            const browserLang = (navigator.language || navigator.userLanguage || "pt").toLowerCase();
            if (browserLang.startsWith("ja")) {
                targetLang = "ja";
            } else if (browserLang.startsWith("pt")) {
                targetLang = "pt";
            } else if (browserLang.startsWith("es")) {
                targetLang = "es";
            } else if (browserLang.startsWith("en")) {
                targetLang = "en";
            }
        }

        // Se o idioma detectado for diferente do atual do template, redireciona
        if (targetLang && targetLang !== window.CURRENT_LANG) {
            const url = new URL(window.location.href);
            url.searchParams.set("lang", targetLang);
            window.location.replace(url.toString());
        }
    } else {
        // Se já tem parâmetro explícito, salva na preferência do usuário
        localStorage.setItem("preferred_lang", urlParams.get("lang"));
    }
})();
