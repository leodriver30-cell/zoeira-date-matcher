"""
Módulo de Internacionalização (i18n) Completo
Idiomas suportados: Português (pt), Japonês (ja), Inglês (en), Espanhol (es)
"""
import datetime
from zoneinfo import ZoneInfo

SUPPORTED_LANGUAGES = ["pt", "ja", "en", "es"]
DEFAULT_LANGUAGE = "pt"

FALLBACK_TIMEZONES = {
    "ja": "Asia/Tokyo",
    "en": "America/New_York",
    "es": "Europe/Madrid",
    "pt": "America/Sao_Paulo",
}

DATE_DURATION_MIN = 180  # 3 horas padrão

TZ_CITY_NAMES = {
    "Asia/Tokyo": {"pt": "Tóquio, Japão", "ja": "日本・東京", "en": "Tokyo, Japan", "es": "Tokio, Japón"},
    "America/New_York": {"pt": "Nova York, EUA", "ja": "米国・ニューヨーク", "en": "New York, USA", "es": "Nueva York, EE. UU."},
    "America/Chicago": {"pt": "Chicago, EUA", "ja": "米国・シカゴ", "en": "Chicago, USA", "es": "Chicago, EE. UU."},
    "America/Denver": {"pt": "Denver, EUA", "ja": "米国・デンバー", "en": "Denver, USA", "es": "Denver, EE. UU."},
    "America/Los_Angeles": {"pt": "Los Angeles, EUA", "ja": "米国・ロサンゼルス", "en": "Los Angeles, USA", "es": "Los Ángeles, EE. UU."},
    "Europe/Madrid": {"pt": "Madrid, Espanha", "ja": "スペイン・マドリード", "en": "Madrid, Spain", "es": "Madrid, España"},
    "America/Sao_Paulo": {"pt": "Brasília, Brasil", "ja": "ブラジル・ブラジリア", "en": "Brasília, Brazil", "es": "Brasilia, Brasil"},
    "Europe/Lisbon": {"pt": "Lisboa, Portugal", "ja": "ポルトガル・リスボン", "en": "Lisbon, Portugal", "es": "Lisboa, Portugal"},
    "Europe/London": {"pt": "Londres, Reino Unido", "ja": "英国・ロンドン", "en": "London, UK", "es": "Londres, Reino Unido"},
}

TRANSLATIONS = {
    "pt": {
        "lang_name": "Português",
        "flag": "🇧🇷",
        "app_title": "Zoeira & Date Match",
        "hero_badge": "✨ Criador de Links Divertidos",
        "hero_title": "Zoeira com Amigos ou Date Perfeito?",
        "hero_desc": "Crie links interativos onde o botão 'Não' foge e torna o 'SIM' inevitável! 🐱💨",
        "create_prank_tab": "Modo Zoeira (Amigos)",
        "create_date_tab": "Modo Date Romântico",
        "custom_question_label": "Qual a pergunta da zoeira?",
        "default_prank_question": "Você é gay?",
        "prank_template_gay": "Você é gay?",
        "prank_template_lunch": "Você me deve um lanche?",
        "prank_template_ugly": "Eu sou mais bonito que você?",
        "suggestions_label": "Sugestões:",
        "target_name_label": "Nome da pretendente / crush:",
        "target_name_placeholder": "Ex: Sakura, Camila, Maria",
        "creator_name_label": "Seu nome:",
        "creator_name_placeholder": "Ex: Leo",
        "date_style_label": "Pergunta do convite:",
        "default_date_question": "{name}, você aceita ter um encontro especial comigo?",
        "contact_section_title": "🔔 Onde você deseja ser avisado quando ela confirmar?",
        "contact_whatsapp_label": "💬 WhatsApp (com código do país e DDD):",
        "contact_whatsapp_placeholder": "Ex: 5511999998888",
        "contact_facebook_label": "💬 Facebook Messenger (usuário ou link):",
        "contact_facebook_placeholder": "Ex: usuario.facebook ou m.me/usuario",
        "contact_line_label": "🟢 LINE (ID ou link de amizade):",
        "contact_line_placeholder": "Ex: seu_id_line ou https://line.me/ti/p/...",
        "contact_callmebot_label": "🤖 Chave do Robô WhatsApp (CallMeBot) - Opcional:",
        "contact_callmebot_placeholder": "Ex: 123456 (ou deixe vazio se já configurado)",
        "contact_callmebot_hint": "Para ativar o robô 100% automático: envie 'I allow callmebot to send me messages' para +34 941 01 99 99 no WhatsApp.",
        "availability_section_title": "📅 Escolha até 10 dias e horários em que você está livre:",
        "availability_section_desc": "Quem receber o convite verá apenas os dias e horários que você liberar abaixo!",
        "days_selected_counter": "{count}/10 dias selecionados",
        "max_days_reached": "Você já escolheu o limite máximo de 10 dias!",
        "select_times_for_day": "Horários disponíveis para {date}:",
        "apply_times_all_days": "✨ Copiar estes horários para todos os dias marcados",
        "add_custom_time_btn": "+ Horário",
        "date_duration_notice": "⏳ Duração padrão do date: 3 horas",
        "timezone_auto_notice": "🕐 Horários no fuso: {tz}",
        "error_select_at_least_one_day": "Por favor, escolha pelo menos 1 dia e 1 horário livre para o encontro!",
        "error_day_without_time": "O dia {date} está sem nenhum horário marcado. Escolha pelo menos 1 horário!",
        "slot_already_taken": "Esse horário acabou de ser escolhido! Por favor, escolha outro horário.",
        "pick_day_first_hint": "👆 Toque em um dos dias acima para ver os horários disponíveis",
        "choose_exact_time_label": "Escolha o horário (duração de 3h):",
        "weekdays_short": ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"],
        "months": ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
        "month_filter_all": "Todos os Meses",
        "days_ahead_horizon_notice": "📅 Você pode escolher datas nos próximos 3 meses:",
        "generate_link_btn": "Gerar Link Especial 🚀",
        "creating_btn": "Criando...",
        "error_create_link": "Erro ao criar link. Tente novamente.",
        "link_created_success": "🎉 Link Criado com Sucesso!",
        "copy_link_btn": "Copiar Link 📋",
        "open_link_btn": "Abrir Link 🔗",
        "dashboard_link_btn": "Ir para Painel de Respostas 📊",
        "btn_yes": "SIM! ❤️",
        "btn_no": "Não",
        "btn_yes_prank": "SIM 😂",
        "btn_no_prank": "NÃO",
        "prank_hint_initial": "Seja sincero... você não tem outra escolha! 😂",
        "prank_hints": [
            "Tentou clicar no Não? Nem tenta! 😂",
            "Errou feio! O botão correu! 🏃💨",
            "Não tem jeito, você vai ter que clicar em SIM!",
            "Epa! Chegou perto, mas escapou!",
            "Desiste, amigo... assume logo! 🌈"
        ],
        "prank_hint_hidden": "O botão 'Não' ficou com medo e se escondeu atrás do 'SIM'! Agora só resta aceitar! 😂🫣",
        "cat_warning_1": "Ei! Não faz isso! 🐾",
        "cat_warning_2": "Ops! Errou de novo! 🐱",
        "cat_warning_final": "O gatinho travesso levou o botão 'Não' embora! Só sobrou o SIM! 🐱❤️",
        "cat_notice_disappeared": "🐾 O botão 'Não' já era!",
        "date_hint_initial": "Dica: Um date inesquecível está esperando por você! ✨",
        "prank_win_title": "EU SABIA! KKKKKK 😂",
        "prank_win_subtitle": "Você tentou clicar em 'Não' {count} vezes antes de aceitar a verdade!",
        "prank_try_another": "Pegar outro amigo agora! 🚀",
        "prank_share_screenshot": "Compartilhar meu print 📸",
        "prank_share_alert": "Você tentou clicar em 'Não' {count} vezes! Tire um print e envie para seu amigo! 😂",
        "date_schedule_title": "Escolha o melhor dia para o nosso encontro! ✨",
        "date_schedule_subtitle": "{creator} liberou estes dias e horários especiais para você escolher! 🥂",
        "calendar_available": "Disponível ✨",
        "calendar_busy": "Ocupado",
        "calendar_selected": "Data Escolhida: {date}",
        "time_slot_label": "Qual o melhor período?",
        "time_slot_night": "Noite (a partir das 19h)",
        "time_slot_afternoon": "Tarde (a partir das 14h)",
        "time_slot_morning": "Manhã / Almoço",
        "confirm_date_btn": "Confirmar Date com {name} 🥂",
        "scheduling_status": "Agendando e avisando ele... 💖",
        "error_confirm_date": "Erro ao confirmar data. Tente novamente.",
        "date_confirmed_title": "Date Confirmado! 🎉💖",
        "date_confirmed_subtitle": "Notificação enviada automaticamente para {creator}! Nos vemos em breve!",
        "dash_test_bot_btn": "🧪 Testar Robô (WhatsApp)",
        "test_bot_sent_success": "Disparo enviado com sucesso! Verifique seu WhatsApp/Facebook.",
        "cat_speech": "Esse 'NÃO' agora é meu! 😼💨",
        "our_date_label": "Nosso Encontro:",
        "add_to_gcal_btn": "📅 Adicionar ao meu Google Calendar",
        "send_confirmation_channel_title": "Avise {creator} com 1 toque:",
        "send_line_btn": "Falar com {creator} no LINE 🟢",
        "line_copied_toast": "Mensagem copiada! Adicione no LINE e cole na conversa com {creator}! 💖",
        "send_whatsapp_btn": "Enviar pelo WhatsApp 💬",
        "send_messenger_btn": "Enviar pelo Messenger 💬",
        "copy_message_btn": "Copiar Mensagem Pronta 📋",
        "message_copied": "Mensagem copiada com sucesso!",
        "whatsapp_template": "Oii {creator}! Aceitei seu convite pro date! Escolhi o dia {date} ({time})! 🥂✨",
        "stats_dodges": "Tentativas de fuga",
        "stats_views": "Visualizações",
        "stats_status": "Status",
        "status_accepted": "Aceitou! 💖",
        "status_waiting": "Aguardando resposta 👀",
        "dash_badge": "📊 Painel em Tempo Real",
        "dash_monitoring": "Monitorando:",
        "dash_live_connected": "Conectado ao Vivo",
        "dash_new_link": "Novo Link +",
        "dash_tried_no": "Tentou Não!",
        "dash_history_title": "Histórico de Escolhas do Date",
        "dash_date_booked": "Date Marcado para:",
        "dash_period": "Horário:",
        "dash_dodges": "Esquivas:",
        "dash_confirmed_badge": "Confirmado 🎉",
        "dash_no_responses": "Nenhuma resposta registrada ainda. Quando a pessoa escolher a data, aparecerá aqui na hora!",
        "dash_sent_link": "Link enviado:",
        "dash_live_alert_msg": "🎉 NOTIFICAÇÃO AO VIVO!\n{target} escolheu o dia {date} ({time})!",
        "footer_text": "© 2026 Zoeira & Date Match • Feito para brincar e conquistar ❤️",
        "time_label_night": "Noite",
        "time_label_afternoon": "Tarde",
        "time_label_morning": "Manhã / Almoço"
    },
    "ja": {
        "lang_name": "日本語",
        "flag": "🇯🇵",
        "app_title": "いたずら＆デートプランナー",
        "hero_badge": "✨ 楽しいリンク作成ツール",
        "hero_title": "友達へのいたずら？それとも最高のデート？",
        "hero_desc": "「いいえ」が逃げて「はい」しか選べなくなる魔法のリンクを作ろう！🐱💨",
        "create_prank_tab": "友達へのいたずらモード",
        "create_date_tab": "ロマンチックデートモード",
        "custom_question_label": "いたずらの質問内容：",
        "default_prank_question": "あなたはゲイですか？",
        "prank_template_gay": "あなたはゲイですか？",
        "prank_template_lunch": "私にご飯をおごってくれますか？",
        "prank_template_ugly": "私の方があなたより魅力的ですか？",
        "suggestions_label": "おすすめの質問：",
        "target_name_label": "お相手の名前（好きな人）：",
        "target_name_placeholder": "例：さくら、花子",
        "creator_name_label": "あなたの名前：",
        "creator_name_placeholder": "例：レオ",
        "date_style_label": "デートのお誘いメッセージ：",
        "default_date_question": "{name}ちゃん、僕と特別なデートに行ってくれますか？",
        "contact_section_title": "🔔 お相手がOKした時の通知先：",
        "contact_whatsapp_label": "💬 WhatsApp（国番号付き）：",
        "contact_whatsapp_placeholder": "例：5511999998888",
        "contact_facebook_label": "💬 Facebook Messenger（IDまたはリンク）：",
        "contact_facebook_placeholder": "例：m.me/yourusername",
        "contact_line_label": "🟢 LINE（LINE IDまたは友だち追加URL）：",
        "contact_line_placeholder": "例：line_id または https://line.me/ti/p/...",
        "contact_callmebot_label": "🤖 WhatsAppボットキー（CallMeBot）- 任意：",
        "contact_callmebot_placeholder": "例：123456（設定済みの場合は空欄でOK）",
        "contact_callmebot_hint": "WhatsAppで自動通知を受け取るには：+34 941 01 99 99 に「I allow callmebot to send me messages」と送信してください。",
        "availability_section_title": "📅 空いている日と時間を最大10日まで選んでください：",
        "availability_section_desc": "お相手には、あなたがここで選んだ日と時間だけが表示されます！",
        "days_selected_counter": "選択中：{count}/10 日",
        "max_days_reached": "最大10日まで選択できます！",
        "select_times_for_day": "{date} の空き時間：",
        "apply_times_all_days": "✨ この時間をすべての選択日にコピーする",
        "add_custom_time_btn": "+ 時間追加",
        "date_duration_notice": "⏳ デートの所要時間：3時間",
        "timezone_auto_notice": "🕐 タイムゾーン：{tz}",
        "error_select_at_least_one_day": "デートのために少なくとも1つの日と時間を選択してください！",
        "error_day_without_time": "{date} の時間が選択されていません。少なくとも1つ選んでください！",
        "slot_already_taken": "この時間はすでに選ばれました！別の時間を選んでください。",
        "pick_day_first_hint": "👆 上の日付をタップして、空いている時間を選んでください",
        "choose_exact_time_label": "時間を選んでください（3時間）：",
        "weekdays_short": ["月", "火", "水", "木", "金", "土", "日"],
        "months": ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
        "month_filter_all": "すべての月",
        "days_ahead_horizon_notice": "📅 今後3ヶ月以内の日程を選択できます：",
        "generate_link_btn": "専用リンクを作成する 🚀",
        "creating_btn": "作成中...",
        "error_create_link": "リンク作成に失敗しました。もう一度お試しください。",
        "link_created_success": "🎉 リンクが完成しました！",
        "copy_link_btn": "リンクをコピー 📋",
        "open_link_btn": "リンクを開く 🔗",
        "dashboard_link_btn": "回答ダッシュボードを見る 📊",
        "btn_yes": "はい！ ❤️",
        "btn_no": "いいえ",
        "btn_yes_prank": "はい 😂",
        "btn_no_prank": "いいえ",
        "prank_hint_initial": "素直になりましょう…他の選択肢はありません！😂",
        "prank_hints": [
            "「いいえ」を押そうとしても無駄ですよ！😂",
            "おっと！ボタンが逃げました！🏃💨",
            "逃げられませんよ、「はい」を押してください！",
            "惜しい！でも届きません！",
            "諦めて真実を認めましょう！🌈"
        ],
        "prank_hint_hidden": "「いいえ」ボタンが怖がって「はい」の後ろに隠れました！もう「はい」を押すしかありません！😂🫣",
        "cat_warning_1": "にゃっ！押せません！🐾",
        "cat_warning_2": "おっと！また外れたにゃ！🐱",
        "cat_warning_final": "いたずら子猫が「いいえ」ボタンを持っていっちゃいました！「はい」しか選べません！🐱❤️",
        "cat_notice_disappeared": "🐾 「いいえ」ボタンは消えちゃいました！",
        "date_hint_initial": "ヒント：素敵なデートが待っていますよ！✨",
        "prank_win_title": "やっぱりね！大成功！笑 😂",
        "prank_win_subtitle": "真実を受け入れるまで「いいえ」を {count} 回押そうとしましたね！",
        "prank_try_another": "別の友達にも送る！ 🚀",
        "prank_share_screenshot": "結果をスクショして送る 📸",
        "prank_share_alert": "「いいえ」を {count} 回押そうとしました！スクショして友達に送りましょう！😂",
        "date_schedule_title": "私たちのデートにぴったりの日を選んでね！✨",
        "date_schedule_subtitle": "{creator} が空いている日と時間を共有してくれました！都合の良い日時を選んでね！🥂",
        "calendar_available": "空きあり ✨",
        "calendar_busy": "予定あり",
        "calendar_selected": "選択した日程：{date}",
        "time_slot_label": "都合の良い時間帯は？",
        "time_slot_night": "夜（19:00〜）",
        "time_slot_afternoon": "午後（14:00〜）",
        "time_slot_morning": "昼 / ランチ",
        "confirm_date_btn": "{name}とのデートを確定する 🥂",
        "scheduling_status": "スケジュール確定＆通知送信中... 💖",
        "error_confirm_date": "確定に失敗しました。もう一度お試しください。",
        "date_confirmed_title": "デート確定！やったね！🎉💖",
        "date_confirmed_subtitle": "{creator} に自動で通知が送られました！当日を楽しみにしています！",
        "dash_test_bot_btn": "🧪 ボット通知テスト（WhatsApp）",
        "test_bot_sent_success": "通知リクエストを送信しました！WhatsAppをご確認ください。",
        "cat_speech": "「『いいえ』はボクがもらったにゃ！🐾」",
        "our_date_label": "私たちのデート：",
        "add_to_gcal_btn": "📅 私のGoogleカレンダーに追加する",
        "send_confirmation_channel_title": "ワンタップで {creator} に返信メッセージを送る：",
        "send_line_btn": "{creator} とLINEで連絡する 🟢",
        "line_copied_toast": "メッセージをコピーしました！LINEで友だち追加してトークに貼ってね！💖",
        "send_whatsapp_btn": "WhatsAppで送信する 💬",
        "send_messenger_btn": "Messengerで送信する 💬",
        "copy_message_btn": "メッセージをコピー 📋",
        "message_copied": "メッセージをコピーしました！",
        "whatsapp_template": "{creator}さん、こんにちは！デートのお誘いOKです！{date}（{time}）にしましょう！✨🥂",
        "stats_dodges": "回避回数",
        "stats_views": "アクセス数",
        "stats_status": "ステータス",
        "status_accepted": "OKしてくれました！💖",
        "status_waiting": "返信待ち 👀",
        "dash_badge": "📊 リアルタイムダッシュボード",
        "dash_monitoring": "監視中のリンク：",
        "dash_live_connected": "ライブ接続中",
        "dash_new_link": "新しいリンクを作成 +",
        "dash_tried_no": "「いいえ」を押そうとしました！",
        "dash_history_title": "デート日程の選択履歴",
        "dash_date_booked": "確定したデート日程：",
        "dash_period": "時間：",
        "dash_dodges": "回避数：",
        "dash_confirmed_badge": "確定済み 🎉",
        "dash_no_responses": "まだ返信がありません。お相手が日程を選ぶとここに即座に表示されます！",
        "dash_sent_link": "送信したリンク：",
        "dash_live_alert_msg": "🎉 速報通知！\n{target}さんが {date}（{time}）を選びました！",
        "footer_text": "© 2026 いたずら＆デートプランナー • 笑顔と恋のために ❤️",
        "time_label_night": "夜",
        "time_label_afternoon": "午後",
        "time_label_morning": "昼 / ランチ"
    },
    "en": {
        "lang_name": "English",
        "flag": "🇺🇸",
        "app_title": "Prank & Date Matcher",
        "hero_badge": "✨ Playful Link Creator",
        "hero_title": "Prank with Friends or the Perfect Date?",
        "hero_desc": "Create interactive links where the 'No' button dodges, making 'YES' inevitable! 🐱💨",
        "create_prank_tab": "Prank Mode (Friends)",
        "create_date_tab": "Romantic Date Mode",
        "custom_question_label": "Prank Question:",
        "default_prank_question": "Are you gay?",
        "prank_template_gay": "Are you gay?",
        "prank_template_lunch": "Do you owe me lunch?",
        "prank_template_ugly": "Am I prettier than you?",
        "suggestions_label": "Suggestions:",
        "target_name_label": "Crush / Date's name:",
        "target_name_placeholder": "e.g. Sakura, Emily, Jessica",
        "creator_name_label": "Your name:",
        "creator_name_placeholder": "e.g. Leo",
        "date_style_label": "Invitation message:",
        "default_date_question": "{name}, will you do me the honor of going on a special date with me?",
        "contact_section_title": "🔔 Where should we notify you when they confirm?",
        "contact_whatsapp_label": "💬 WhatsApp (with country code):",
        "contact_whatsapp_placeholder": "e.g. 15551234567",
        "contact_facebook_label": "💬 Facebook Messenger (username or link):",
        "contact_facebook_placeholder": "e.g. m.me/username",
        "contact_line_label": "🟢 LINE (ID or friend link):",
        "contact_line_placeholder": "e.g. line_id or https://line.me/ti/p/...",
        "contact_callmebot_label": "🤖 WhatsApp Bot Key (CallMeBot) - Optional:",
        "contact_callmebot_placeholder": "e.g. 123456 (or leave blank if pre-configured)",
        "contact_callmebot_hint": "To receive auto WhatsApp alerts: send 'I allow callmebot to send me messages' to +34 941 01 99 99 on WhatsApp.",
        "availability_section_title": "📅 Pick up to 10 days and times when you're free:",
        "availability_section_desc": "Your date will only see the days and times you unlock below!",
        "days_selected_counter": "{count}/10 days selected",
        "max_days_reached": "You've reached the maximum of 10 days!",
        "select_times_for_day": "Available times for {date}:",
        "apply_times_all_days": "✨ Copy these times to all selected days",
        "add_custom_time_btn": "+ Add time",
        "date_duration_notice": "⏳ Default date duration: 3 hours",
        "timezone_auto_notice": "🕐 Times shown in: {tz}",
        "error_select_at_least_one_day": "Please select at least 1 day and 1 available time for the date!",
        "error_day_without_time": "Day {date} has no times selected. Please pick at least 1 time!",
        "slot_already_taken": "That time slot was just taken! Please pick another time.",
        "pick_day_first_hint": "👆 Tap one of the days above to see available times",
        "choose_exact_time_label": "Pick a time (3h duration):",
        "weekdays_short": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        "month_filter_all": "All Months",
        "days_ahead_horizon_notice": "📅 You can choose dates within the next 3 months:",
        "generate_link_btn": "Generate Special Link 🚀",
        "creating_btn": "Creating...",
        "error_create_link": "Error creating link. Please try again.",
        "link_created_success": "🎉 Link Created Successfully!",
        "copy_link_btn": "Copy Link 📋",
        "open_link_btn": "Open Link 🔗",
        "dashboard_link_btn": "Go to Dashboard 📊",
        "btn_yes": "YES! ❤️",
        "btn_no": "No",
        "btn_yes_prank": "YES 😂",
        "btn_no_prank": "NO",
        "prank_hint_initial": "Be honest... you don't have another choice! 😂",
        "prank_hints": [
            "Trying to click No? Don't even try! 😂",
            "Missed it! The button ran away! 🏃💨",
            "No way out, you must click YES!",
            "Whoops! Close, but escaped!",
            "Give up, friend... accept the truth! 🌈"
        ],
        "prank_hint_hidden": "The 'No' button got scared and hid behind 'YES'! Now you have no choice! 😂🫣",
        "cat_warning_1": "Hey! You can't click that! 🐾",
        "cat_warning_2": "Oops! Missed again! 🐱",
        "cat_warning_final": "The mischievous kitten stole the 'No' button! Only 'YES' is left! 🐱❤️",
        "cat_notice_disappeared": "🐾 The 'No' button is gone!",
        "date_hint_initial": "Hint: An unforgettable date awaits you! ✨",
        "prank_win_title": "I KNEW IT! HAHAHA 😂",
        "prank_win_subtitle": "You tried clicking 'No' {count} times before accepting the truth!",
        "prank_try_another": "Prank another friend now! 🚀",
        "prank_share_screenshot": "Share my screenshot 📸",
        "prank_share_alert": "You tried clicking 'No' {count} times! Take a screenshot and send it to your friend! 😂",
        "date_schedule_title": "Pick the perfect day for our date! ✨",
        "date_schedule_subtitle": "{creator} connected availability so you can choose the ideal day! 🥂",
        "calendar_available": "Available ✨",
        "calendar_busy": "Busy",
        "calendar_selected": "Selected Date: {date}",
        "time_slot_label": "Preferred time?",
        "time_slot_night": "Evening (7:00 PM onwards)",
        "time_slot_afternoon": "Afternoon (2:00 PM onwards)",
        "time_slot_morning": "Morning / Lunch",
        "confirm_date_btn": "Confirm Date with {name} 🥂",
        "scheduling_status": "Scheduling and notifying them... 💖",
        "error_confirm_date": "Error confirming date. Please try again.",
        "date_confirmed_title": "Date Confirmed! 🎉💖",
        "date_confirmed_subtitle": "Notification automatically sent to {creator}! See you soon!",
        "date_notified_automatically": "Notification sent automatically by the bot to {creator}'s WhatsApp/Facebook! All set!",
        "cat_speech": "That 'NO' is mine now! 😼💨",
        "our_date_label": "Our Date:",
        "add_to_gcal_btn": "📅 Add to my Google Calendar",
        "send_confirmation_channel_title": "Send your confirmation to {creator} in 1 tap:",
        "send_line_btn": "Chat with {creator} on LINE 🟢",
        "line_copied_toast": "Message copied! Add on LINE and paste into chat with {creator}! 💖",
        "send_whatsapp_btn": "Send via WhatsApp 💬",
        "send_messenger_btn": "Send via Messenger 💬",
        "copy_message_btn": "Copy Ready Message 📋",
        "message_copied": "Message copied to clipboard!",
        "whatsapp_template": "Hey {creator}! I'd love to go on a date with you! I picked {date} ({time})! 🥂✨",
        "stats_dodges": "Escape attempts",
        "stats_views": "Views",
        "stats_status": "Status",
        "status_accepted": "Accepted! 💖",
        "status_waiting": "Waiting for response 👀",
        "dash_badge": "📊 Real-Time Dashboard",
        "dash_monitoring": "Monitoring:",
        "dash_live_connected": "Connected Live",
        "dash_new_link": "New Link +",
        "dash_tried_no": "Tried No!",
        "dash_history_title": "Date Scheduling History",
        "dash_date_booked": "Date Booked for:",
        "dash_period": "Time:",
        "dash_dodges": "Dodges:",
        "dash_confirmed_badge": "Confirmed 🎉",
        "dash_no_responses": "No responses yet. When they pick a date, it will appear here instantly!",
        "dash_sent_link": "Sent link:",
        "dash_live_alert_msg": "🎉 LIVE ALERT!\n{target} picked {date} ({time})!",
        "footer_text": "© 2026 Prank & Date Matcher • Made for laughs and love ❤️",
        "time_label_night": "Evening",
        "time_label_afternoon": "Afternoon",
        "time_label_morning": "Morning / Lunch"
    },
    "es": {
        "lang_name": "Español",
        "flag": "🇪🇸",
        "app_title": "Bromas & Citas Divertidas",
        "hero_badge": "✨ Creador de Enlaces Divertidos",
        "hero_title": "¿Broma con Amigos o la Cita Perfecta?",
        "hero_desc": "¡Crea enlaces interactivos donde el botón 'No' huye y hace inevitable el 'SÍ'! 🐱💨",
        "create_prank_tab": "Modo Broma (Amigos)",
        "create_date_tab": "Modo Cita Romántica",
        "custom_question_label": "¿Cuál es la pregunta de la broma?",
        "default_prank_question": "¿Eres gay?",
        "prank_template_gay": "¿Eres gay?",
        "prank_template_lunch": "¿Me debes una pizza?",
        "prank_template_ugly": "¿Soy más guapo que tú?",
        "suggestions_label": "Sugerencias:",
        "target_name_label": "Nombre de tu crush:",
        "target_name_placeholder": "Ej: Sakura, Camila, Sofía",
        "creator_name_label": "Tu nombre:",
        "creator_name_placeholder": "Ej: Leo",
        "date_style_label": "Pregunta de la invitación:",
        "default_date_question": "{name}, ¿aceptarías tener una cita especial conmigo?",
        "contact_section_title": "🔔 ¿Dónde quieres ser avisado cuando ella confirme?",
        "contact_whatsapp_label": "💬 WhatsApp (con código de país):",
        "contact_whatsapp_placeholder": "Ej: 34612345678",
        "contact_facebook_label": "💬 Facebook Messenger (usuario o enlace):",
        "contact_facebook_placeholder": "Ej: m.me/usuario",
        "contact_line_label": "🟢 LINE (ID o enlace de amigo):",
        "contact_line_placeholder": "Ej: line_id o https://line.me/ti/p/...",
        "contact_callmebot_label": "🤖 Clave Bot WhatsApp (CallMeBot) - Opcional:",
        "contact_callmebot_placeholder": "Ej: 123456 (o dejar en blanco si ya configurado)",
        "contact_callmebot_hint": "Para recibir en WhatsApp automáticamente: envía 'I allow callmebot to send me messages' al +34 941 01 99 99 en WhatsApp.",
        "availability_section_title": "📅 Elige hasta 10 días y horarios en los que estás libre:",
        "availability_section_desc": "¡Tu cita solo verá los días y horarios que habilites aquí abajo!",
        "days_selected_counter": "{count}/10 días seleccionados",
        "max_days_reached": "¡Ya alcanzaste el límite máximo de 10 días!",
        "select_times_for_day": "Horarios disponibles para {date}:",
        "apply_times_all_days": "✨ Copiar estos horarios a todos los días seleccionados",
        "add_custom_time_btn": "+ Horario",
        "date_duration_notice": "⏳ Duración estándar de la cita: 3 horas",
        "timezone_auto_notice": "🕐 Horarios en zona horaria: {tz}",
        "error_select_at_least_one_day": "¡Por favor, elige al menos 1 día y 1 horario libre para la cita!",
        "error_day_without_time": "El día {date} no tiene horarios marcados. ¡Elige al menos 1 horario!",
        "slot_already_taken": "¡Ese horario acaba de ser elegido! Por favor, elige otro.",
        "pick_day_first_hint": "👆 Toca uno de los días de arriba para ver los horarios disponibles",
        "choose_exact_time_label": "Elige el horario (duración de 3h):",
        "weekdays_short": ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
        "months": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
        "month_filter_all": "Todos los Meses",
        "days_ahead_horizon_notice": "📅 Puedes elegir fechas dentro de los próximos 3 meses:",
        "generate_link_btn": "Generar Enlace Especial 🚀",
        "creating_btn": "Creando...",
        "error_create_link": "Error al crear el enlace. Inténtalo de nuevo.",
        "link_created_success": "¡Tu enlace está listo! 🎉",
        "copy_link_btn": "Copiar Enlace 📋",
        "open_link_btn": "Abrir Enlace 🔗",
        "dashboard_link_btn": "Ir al Panel de Respuestas 📊",
        "btn_yes": "¡SÍ! ❤️",
        "btn_no": "No",
        "btn_yes_prank": "SÍ 😂",
        "btn_no_prank": "NO",
        "prank_hint_initial": "Sé sincero... ¡no tienes otra opción! 😂",
        "prank_hints": [
            "¿Intentaste hacer clic en No? ¡Ni lo intentes! 😂",
            "¡Fallaste! ¡El botón se escapó! 🏃💨",
            "¡No hay escapatoria, tendrás que presionar SÍ!",
            "¡Upa! Estuvo cerca, ¡pero escapó!",
            "¡Ríndete, amigo... acepta la verdad! 🌈"
        ],
        "prank_hint_hidden": "¡El botón 'No' tuvo miedo y se escondió detrás del 'SÍ'! ¡Ahora no tienes opción! 😂🫣",
        "cat_warning_1": "¡Ey! ¡No toques ahí! 🐾",
        "cat_warning_2": "¡Ups! ¡Fallaste de nuevo! 🐱",
        "cat_warning_final": "¡El gatito travieso se llevó el botón 'No'! ¡Solo queda el SÍ! 🐱❤️",
        "cat_notice_disappeared": "🐾 ¡El botón 'No' desapareció!",
        "date_hint_initial": "Pista: ¡Una cita inolvidable te está esperando! ✨",
        "prank_win_title": "¡LO SABÍA! JAJAJA 😂",
        "prank_win_subtitle": "¡Intentaste hacer clic en 'No' {count} veces antes de aceptar la verdad!",
        "prank_try_another": "¡Hacer una broma a otro amigo ahora! 🚀",
        "prank_share_screenshot": "Compartir captura de pantalla 📸",
        "prank_share_alert": "¡Intentaste presionar 'No' {count} veces! ¡Toma una captura y mándasela a tu amigo! 😂",
        "date_schedule_title": "¡Elige el mejor día para nuestra cita! ✨",
        "date_schedule_subtitle": "{creator} conectó su disponibilidad para que elijas el día ideal! 🥂",
        "calendar_available": "Disponible ✨",
        "calendar_busy": "Ocupado",
        "calendar_selected": "Fecha Seleccionada: {date}",
        "time_slot_label": "¿Cuál es el mejor momento?",
        "time_slot_night": "Noche (desde las 19:00)",
        "time_slot_afternoon": "Tarde (desde las 14:00)",
        "time_slot_morning": "Mañana / Almuerzo",
        "confirm_date_btn": "Confirmar Cita con {name} 🥂",
        "scheduling_status": "Agendando y avisándole... 💖",
        "error_confirm_date": "Error al confirmar la fecha. Inténtalo de nuevo.",
        "date_confirmed_title": "¡Cita Confirmada! 🎉💖",
        "date_confirmed_subtitle": "¡Notificación enviada automáticamente a {creator}! ¡Nos vemos pronto!",
        "date_notified_automatically": "¡Notificación enviada automáticamente por el bot al WhatsApp/Facebook de {creator}! ¡Todo listo!",
        "dash_test_bot_btn": "🧪 Probar Bot (WhatsApp)",
        "test_bot_sent_success": "¡Notificación de prueba enviada! Revisa tu WhatsApp/Facebook.",
        "cat_speech": "¡Ese 'NO' ahora es mío! 😼💨",
        "our_date_label": "Nuestra Cita:",
        "add_to_gcal_btn": "📅 Agregar a mi Google Calendar",
        "send_confirmation_channel_title": "Envía la confirmación a {creator} en 1 toque:",
        "send_line_btn": "Hablar con {creator} en LINE 🟢",
        "line_copied_toast": "¡Mensaje copiado! Añade en LINE y pega en la conversación con {creator}! 💖",
        "send_whatsapp_btn": "Enviar por WhatsApp 💬",
        "send_messenger_btn": "Enviar por Messenger 💬",
        "copy_message_btn": "Copiar Mensaje Listo 📋",
        "message_copied": "¡Mensaje copiado con éxito!",
        "whatsapp_template": "¡Hola {creator}! ¡Acepto la cita! Elegí el día {date} ({time})! 🥂✨",
        "stats_dodges": "Intentos de escape",
        "stats_views": "Vistas",
        "stats_status": "Estado",
        "status_accepted": "¡Aceptó! 💖",
        "status_waiting": "Esperando respuesta 👀",
        "dash_badge": "📊 Panel en Tiempo Real",
        "dash_monitoring": "Monitoreando:",
        "dash_live_connected": "Conectado en Vivo",
        "dash_new_link": "Nuevo Enlace +",
        "dash_tried_no": "¡Intentó No!",
        "dash_history_title": "Historial de Citas Agendadas",
        "dash_date_booked": "Cita Agendada para:",
        "dash_period": "Horario:",
        "dash_dodges": "Esquivas:",
        "dash_confirmed_badge": "Confirmado 🎉",
        "dash_no_responses": "Aún no hay respuestas. ¡Cuando elijan fecha aparecerá aquí al instante!",
        "dash_sent_link": "Enlace enviado:",
        "dash_live_alert_msg": "🎉 ¡ALERTA EN VIVO!\n{target} eligió el día {date} ({time})!",
        "footer_text": "© 2026 Bromas & Citas Divertidas • Hecho para sonreír y enamorar ❤️",
        "time_label_night": "Noche",
        "time_label_afternoon": "Tarde",
        "time_label_morning": "Mañana / Almuerzo"
    }
}

def resolve_timezone(client_tz: str | None = None, lang: str = "pt") -> str:
    """
    Valida o fuso horário informado pelo navegador do convidante.
    Caso seja inválido ou ausente, aplica a regra de reserva pelo idioma:
    ja -> Asia/Tokyo, en -> America/New_York, es -> Europe/Madrid, pt -> America/Sao_Paulo.
    """
    clean_lang = (lang or DEFAULT_LANGUAGE).lower()
    if clean_lang not in SUPPORTED_LANGUAGES:
        clean_lang = DEFAULT_LANGUAGE

    if client_tz and isinstance(client_tz, str):
        candidate = client_tz.strip()
        if 1 < len(candidate) <= 64 and "/" in candidate:
            try:
                ZoneInfo(candidate)
                return candidate
            except Exception:
                pass
            if candidate in TZ_CITY_NAMES:
                return candidate

    return FALLBACK_TIMEZONES.get(clean_lang, FALLBACK_TIMEZONES[DEFAULT_LANGUAGE])

def format_tz_label(tz_name: str | None, lang: str = "pt", ref_dt: datetime.datetime | None = None) -> str:
    """
    Formata o nome amigável do fuso horário + deslocamento UTC real (incluindo horário de verão).
    Ex: 'Tóquio, Japão (UTC+9)' ou 'Nova York, EUA (UTC-4)'.
    """
    clean_lang = (lang or DEFAULT_LANGUAGE).lower()
    if clean_lang not in SUPPORTED_LANGUAGES:
        clean_lang = DEFAULT_LANGUAGE

    resolved = resolve_timezone(tz_name, clean_lang)
    city_map = TZ_CITY_NAMES.get(resolved)
    if city_map:
        city_label = city_map.get(clean_lang, city_map["pt"])
    else:
        city_label = resolved.split("/")[-1].replace("_", " ")

    try:
        zi = ZoneInfo(resolved)
        now_tz = (ref_dt.astimezone(zi) if ref_dt else datetime.datetime.now(zi))
        offset = now_tz.utcoffset()
        if offset is not None:
            total_minutes = int(offset.total_seconds() // 60)
            sign = "+" if total_minutes >= 0 else "-"
            abs_min = abs(total_minutes)
            hours, mins = divmod(abs_min, 60)
            offset_str = f"UTC{sign}{hours}" if mins == 0 else f"UTC{sign}{hours}:{mins:02d}"
            return f"{city_label} ({offset_str})"
    except Exception:
        pass

    return f"{city_label} ({resolved})"

def format_time_range(start_hhmm: str, duration_min: int = DATE_DURATION_MIN) -> str:
    """
    Dado um horário inicial 'HH:MM' e duração em minutos (padrão 180 = 3h),
    retorna 'HH:MM – HH:MM' (ex: '19:00 – 22:00').
    """
    try:
        parts = start_hhmm.strip().split(":")
        hour = int(parts[0])
        minute = int(parts[1])
        total_end_min = (hour * 60 + minute + duration_min) % (24 * 60)
        end_h, end_m = divmod(total_end_min, 60)
        return f"{hour:02d}:{minute:02d} – {end_h:02d}:{end_m:02d}"
    except Exception:
        return start_hhmm

def detect_language(accept_language_header: str | None = None, query_lang: str | None = None) -> str:
    if query_lang and query_lang.lower() in SUPPORTED_LANGUAGES:
        return query_lang.lower()
    
    if not accept_language_header:
        return DEFAULT_LANGUAGE
    
    header_lower = accept_language_header.lower()
    if "ja" in header_lower:
        return "ja"
    if "pt" in header_lower:
        return "pt"
    if "es" in header_lower:
        return "es"
    if "en" in header_lower:
        return "en"
    
    return DEFAULT_LANGUAGE

def t(key: str, lang: str = "pt", **kwargs) -> str:
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS[DEFAULT_LANGUAGE])
    text = lang_dict.get(key, TRANSLATIONS[DEFAULT_LANGUAGE].get(key, key))
    if isinstance(text, str) and kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text

def get_all_translations_json() -> dict:
    return TRANSLATIONS
