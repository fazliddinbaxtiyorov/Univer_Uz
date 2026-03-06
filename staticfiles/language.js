/* ===================================
   UniBase - Multi-Language System
   Translation management and language switching
   =================================== */

const TRANSLATIONS = {
    en: {
        // Navigation
        nav_tests: 'Tests',
        nav_universities: 'Universities',
        nav_news: 'News',
        nav_features: 'Features',
        nav_support: 'Support',
        nav_login: 'Login',
        nav_register: 'Register',
        nav_dashboard: 'Dashboard',
        nav_logout: 'Logout',
        nav_manage_tests: 'Manage Tests',

        // Hero Section
        hero_title: 'Preparation Like a Real Exam',
        hero_subtitle: 'IELTS, SAT, Milliy certificate, DTM — timed practice tests in a realistic exam environment',
        hero_btn_start: 'Start Free',
        hero_btn_view: 'View Tests',

        // Test Cards
        test_start: 'Start Test',
        test_badge_english: 'ENGLISH',
        test_badge_academic: 'ACADEMIC',
        test_badge_national: 'NATIONAL',
        test_badge_entrance: 'ENTRANCE',
        test_badge_cognitive: 'COGNITIVE',

        // Test Section
        tests_title: 'Choose Your Test',
        test_ielts_title: 'IELTS',
        test_ielts_desc: 'Comprehensive IELTS practice across all sections with realistic exam conditions.',
        test_sat_title: 'SAT',
        test_sat_desc: 'Prepare for SAT with Math and English sections in a timed environment.',
        test_milliy_title: 'Milliy certificate',
        test_milliy_desc: 'National certification exam practice with comprehensive question bank.',
        test_dtm_title: 'DTM',
        test_dtm_desc: 'Prepare for university entrance exams with realistic test simulations.',

        // Features
        features_title: 'Why Choose UniBase?',
        feature_realistic_title: '🎯 Realistic Exam Environment',
        feature_realistic_desc: 'Experience the pressure and atmosphere of real exams with authentic interfaces, timers, and question formats.',
        feature_analytics_title: '📊 Detailed Analytics',
        feature_analytics_desc: 'Track your performance with comprehensive analysis of your strengths, weaknesses, and progress over time.',
        feature_progress_title: '📈 Track Your Progress',
        feature_progress_desc: 'Monitor your improvement with dynamic progress tracking, personalized recommendations, and goal setting.',

        // Login Page
        login_title: 'Welcome Back',
        login_subtitle: 'Login to continue your exam preparation',
        login_email: 'Email Address',
        login_password: 'Password',
        login_remember: 'Remember me',
        login_btn: 'Login',
        login_no_account: "Don't have an account?",
        login_register_here: 'Register here',
        login_demo: 'Demo Credentials:',

        // Register Page
        register_title: 'Create Account',
        register_subtitle: 'Start your exam preparation journey',
        register_name: 'Full Name',
        register_email: 'Email Address',
        register_student_id: 'Student ID (Optional)',
        register_password: 'Password',
        register_confirm: 'Confirm Password',
        register_btn: 'Create Account',
        register_have_account: 'Already have an account?',
        register_login_here: 'Login here',

        // Student Dashboard
        dashboard_welcome: 'Welcome',
        dashboard_subtitle: 'Choose a test to start your practice session',
        dashboard_available_tests: 'Available Tests',
        dashboard_recent_results: 'My Recent Results',
        dashboard_no_tests: 'No tests available yet. Please check back later.',
        dashboard_no_results: "You haven't taken any tests yet. Start practicing to see your results here!",

        // Common
        duration: 'Duration',
        questions: 'Questions',
        minutes: 'minutes',
        footer_rights: 'All rights reserved.',
        footer_copyright: '© 2026 UniBase. All rights reserved.',
        footer_tests: 'Tests',
        footer_features: 'Features',
        footer_privacy: 'Privacy Policy',
        footer_contact: 'Contact',
        home: 'Home',

        // Admin Dashboard
        admin_dashboard_title: 'Admin Dashboard',
        admin_dashboard_subtitle: 'Manage tests and monitor student performance',
        admin_total_tests: 'Total Tests',
        admin_registered_students: 'Registered Students',
        admin_test_attempts: 'Test Attempts',
        admin_quick_actions: 'Quick Actions',
        admin_add_new_test: 'Add New Test',
        admin_add_test_desc: 'Create a new exam for students to practice',
        admin_create_test: 'Create Test',
        admin_manage_tests_title: 'Manage Tests',
        admin_manage_tests_desc: 'View, edit, or delete existing tests',
        admin_view_tests: 'View Tests',
        admin_view_students_title: 'View Students',
        admin_view_students_desc: 'See all registered students and their progress',
        admin_view_students_btn: 'View Students',
        admin_recent_activity: 'Recent Test Activity',
        admin_no_activity: 'No test activity yet.',
        admin_registered_students_title: 'Registered Students',
        admin_no_students: 'No students registered yet.',

        // Admin Tests Management
        admin_tests_manage_title: 'Manage Tests',
        admin_tests_add_new: 'Add New Test',
        admin_tests_create_new: 'Create New Test',
        admin_tests_edit: 'Edit Test',
        admin_tests_test_name: 'Test Name',
        admin_tests_category: 'Category',
        admin_tests_select_category: 'Select category...',
        admin_tests_duration_min: 'Duration (minutes)',
        admin_tests_description: 'Description',
        admin_tests_questions_section: 'Questions',
        admin_tests_add_question: 'Add Question',
        admin_tests_save: 'Save Test',
        admin_tests_cancel: 'Cancel',
        admin_tests_existing: 'Existing Tests',
        admin_tests_no_tests: 'No tests created yet. Click "Add New Test" to create one.',
        admin_tests_edit_btn: 'Edit',
        admin_tests_delete_btn: 'Delete',
        admin_tests_created: 'Created',
        admin_tests_question_text: 'Question Text',
        admin_tests_option: 'Option',
        admin_tests_correct_answer: 'Correct Answer',
        admin_tests_select_correct: 'Select correct answer...',
        admin_tests_remove: 'Remove',
        admin_tests_question: 'Question',

        // Test Taking
        test_taking_loading: 'Loading Test...',
        test_taking_question_of: 'Question',
        test_taking_of: 'of',
        test_taking_pause: 'Pause',
        test_taking_resume: 'Resume',
        test_taking_previous: 'Previous',
        test_taking_next: 'Next',
        test_taking_submit: 'Submit Test',

        // Test Results
        results_title: 'Test Results',
        results_your_score: 'Your Score',
        results_percentage: 'Percentage',
        results_time_taken: 'Time Taken',
        results_answer_review: 'Answer Review',
        results_back_dashboard: 'Back to Dashboard',
        results_print: 'Print Results',
        results_excellent: 'Excellent!',
        results_excellent_msg: 'Outstanding performance!',
        results_good: 'Good Job!',
        results_good_msg: 'You passed the test.',
        results_fair: 'Fair',
        results_fair_msg: 'Consider reviewing the material and trying again.',
        results_keep_practicing: 'Keep Practicing',
        results_practice_msg: 'Review the material and attempt again.',
        results_correct: 'Correct',
        results_incorrect: 'Incorrect',
        results_your_answer: 'Your Answer',
        results_correct_answer: 'Correct Answer',
        results_not_answered: 'Not answered',

        // Table Headers
        table_name: 'Name',
        table_email: 'Email',
        table_student_id: 'Student ID',
        table_registered: 'Registered',
        table_student: 'Student',
        table_test: 'Test',
        table_test_name: 'Test Name',
        table_score: 'Score',
        table_time: 'Time',
        table_date: 'Date',
    },

    ru: {
        // Navigation
        nav_tests: 'Тесты',
        nav_universities: 'Университеты',
        nav_news: 'Новости',
        nav_features: 'Возможности',
        nav_support: 'Поддержка',
        nav_login: 'Войти',
        nav_register: 'Регистрация',
        nav_dashboard: 'Панель',
        nav_logout: 'Выйти',
        nav_manage_tests: 'Управление тестами',

        // Hero Section
        hero_title: 'Подготовка как на реальном экзамене',
        hero_subtitle: 'IELTS, SAT, Milliy certificate, DTM — тесты с таймером в реалистичной экзаменационной среде',
        hero_btn_start: 'Начать бесплатно',
        hero_btn_view: 'Смотреть тесты',

        // Test Cards
        test_start: 'Начать тест',
        test_badge_english: 'АНГЛИЙСКИЙ',
        test_badge_academic: 'АКАДЕМИЧЕСКИЙ',
        test_badge_national: 'НАЦИОНАЛЬНЫЙ',
        test_badge_entrance: 'ВСТУПИТЕЛЬНЫЙ',
        test_badge_cognitive: 'КОГНИТИВНЫЙ',

        // Test Section
        tests_title: 'Выберите свой тест',
        test_ielts_title: 'IELTS',
        test_ielts_desc: 'Всесторонняя практика IELTS по всем разделам с реалистичными условиями экзамена.',
        test_sat_title: 'SAT',
        test_sat_desc: 'Подготовьтесь к SAT с разделами математики и английского языка в условиях ограниченного времени.',
        test_milliy_title: 'Milliy certificate',
        test_milliy_desc: 'Практика национального сертификационного экзамена с полным банком вопросов.',
        test_dtm_title: 'DTM',
        test_dtm_desc: 'Подготовьтесь к вступительным экзаменам в университет с реалистичными симуляциями тестов.',

        // Features
        features_title: 'Почему выбирают UniBase?',
        feature_realistic_title: '🎯 Реалистичная среда экзамена',
        feature_realistic_desc: 'Почувствуйте давление и атмосферу настоящих экзаменов с аутентичными интерфейсами, таймерами и форматами вопросов.',
        feature_analytics_title: '📊 Детальная аналитика',
        feature_analytics_desc: 'Отслеживайте свою успеваемость с помощью комплексного анализа сильных и слабых сторон, а также прогресса.',
        feature_progress_title: '📈 Отслеживание прогресса',
        feature_progress_desc: 'Следите за своим улучшением с помощью динамического отслеживания прогресса и персональных рекомендаций.',

        // Login Page
        login_title: 'С возвращением',
        login_subtitle: 'Войдите, чтобы продолжить подготовку к экзамену',
        login_email: 'Электронная почта',
        login_password: 'Пароль',
        login_remember: 'Запомнить меня',
        login_btn: 'Войти',
        login_no_account: 'Нет аккаунта?',
        login_register_here: 'Зарегистрируйтесь здесь',
        login_demo: 'Демо-учетные данные:',

        // Register Page
        register_title: 'Создать аккаунт',
        register_subtitle: 'Начните свое путешествие по подготовке к экзамену',
        register_name: 'Полное имя',
        register_email: 'Электронная почта',
        register_student_id: 'ID студента (необязательно)',
        register_password: 'Пароль',
        register_confirm: 'Подтвердите пароль',
        register_btn: 'Создать аккаунт',
        register_have_account: 'Уже есть аккаунт?',
        register_login_here: 'Войдите здесь',

        // Student Dashboard
        dashboard_welcome: 'Добро пожаловать',
        dashboard_subtitle: 'Выберите тест, чтобы начать практику',
        dashboard_available_tests: 'Доступные тесты',
        dashboard_recent_results: 'Мои последние результаты',
        dashboard_no_tests: 'Тесты пока недоступны. Пожалуйста, зайдите позже.',
        dashboard_no_results: 'Вы еще не проходили тесты. Начните практиковаться, чтобы увидеть результаты здесь!',

        // Common
        duration: 'Продолжительность',
        questions: 'Вопросы',
        minutes: 'минут',
        footer_rights: 'Все права защищены.',
        footer_copyright: '© 2026 UniBase. Все права защищены.',
        footer_tests: 'Тесты',
        footer_features: 'Возможности',
        footer_privacy: 'Политика конфиденциальности',
        footer_contact: 'Контакты',
        home: 'Главная',

        // Admin Dashboard
        admin_dashboard_title: 'Панель администратора',
        admin_dashboard_subtitle: 'Управление тестами и мониторинг успеваемости студентов',
        admin_total_tests: 'Всего тестов',
        admin_registered_students: 'Зарегистрированных студентов',
        admin_test_attempts: 'Попыток тестирования',
        admin_quick_actions: 'Быстрые действия',
        admin_add_new_test: 'Добавить новый тест',
        admin_add_test_desc: 'Создать новый экзамен для студентов',
        admin_create_test: 'Создать тест',
        admin_manage_tests_title: 'Управление тестами',
        admin_manage_tests_desc: 'Просмотр, редактирование или удаление существующих тестов',
        admin_view_tests: 'Смотреть тесты',
        admin_view_students_title: 'Просмотр студентов',
        admin_view_students_desc: 'Посмотреть всех зарегистрированных студентов и их прогресс',
        admin_view_students_btn: 'Смотреть студентов',
        admin_recent_activity: 'Недавняя активность тестирования',
        admin_no_activity: 'Активности тестирования пока нет.',
        admin_registered_students_title: 'Зарегистрированные студенты',
        admin_no_students: 'Студенты еще не зарегистрированы.',

        // Admin Tests Management
        admin_tests_manage_title: 'Управление тестами',
        admin_tests_add_new: 'Добавить новый тест',
        admin_tests_create_new: 'Создать новый тест',
        admin_tests_edit: 'Редактировать тест',
        admin_tests_test_name: 'Название теста',
        admin_tests_category: 'Категория',
        admin_tests_select_category: 'Выберите категорию...',
        admin_tests_duration_min: 'Продолжительность (минуты)',
        admin_tests_description: 'Описание',
        admin_tests_questions_section: 'Вопросы',
        admin_tests_add_question: 'Добавить вопрос',
        admin_tests_save: 'Сохранить тест',
        admin_tests_cancel: 'Отмена',
        admin_tests_existing: 'Существующие тесты',
        admin_tests_no_tests: 'Тесты еще не созданы. Нажмите «Добавить новый тест», чтобы создать.',
        admin_tests_edit_btn: 'Редактировать',
        admin_tests_delete_btn: 'Удалить',
        admin_tests_created: 'Создано',
        admin_tests_question_text: 'Текст вопроса',
        admin_tests_option: 'Вариант',
        admin_tests_correct_answer: 'Правильный ответ',
        admin_tests_select_correct: 'Выберите правильный ответ...',
        admin_tests_remove: 'Удалить',
        admin_tests_question: 'Вопрос',

        // Test Taking
        test_taking_loading: 'Загрузка теста...',
        test_taking_question_of: 'Вопрос',
        test_taking_of: 'из',
        test_taking_pause: 'Пауза',
        test_taking_resume: 'Продолжить',
        test_taking_previous: 'Предыдущий',
        test_taking_next: 'Следующий',
        test_taking_submit: 'Отправить тест',

        // Test Results
        results_title: 'Результаты теста',
        results_your_score: 'Ваш результат',
        results_percentage: 'Процент',
        results_time_taken: 'Затраченное время',
        results_answer_review: 'Обзор ответов',
        results_back_dashboard: 'Вернуться на панель',
        results_print: 'Печать результатов',
        results_excellent: 'Отлично!',
        results_excellent_msg: 'Выдающийся результат!',
        results_good: 'Хорошая работа!',
        results_good_msg: 'Вы прошли тест.',
        results_fair: 'Удовлетворительно',
        results_fair_msg: 'Рассмотрите возможность повторения материала и попробуйте снова.',
        results_keep_practicing: 'Продолжайте практиковаться',
        results_practice_msg: 'Повторите материал и попробуйте снова.',
        results_correct: 'Правильно',
        results_incorrect: 'Неправильно',
        results_your_answer: 'Ваш ответ',
        results_correct_answer: 'Правильный ответ',
        results_not_answered: 'Не отвечено',

        // Table Headers
        table_name: 'Имя',
        table_email: 'Email',
        table_student_id: 'ID студента',
        table_registered: 'Зарегистрирован',
        table_student: 'Студент',
        table_test: 'Тест',
        table_test_name: 'Название теста',
        table_score: 'Результат',
        table_time: 'Время',
        table_date: 'Дата',
    },

    uz: {
        // Navigation
        nav_tests: 'Testlar',
        nav_universities: 'Universitetlar',
        nav_news: 'Yangiliklar',
        nav_features: "Xususiyatlar",
        nav_support: 'Yordam',
        nav_login: 'Kirish',
        nav_register: "Ro'yxatdan o'tish",
        nav_dashboard: 'Boshqaruv paneli',
        nav_logout: 'Chiqish',
        nav_manage_tests: "Testlarni boshqarish",

        // Hero Section
        hero_title: 'Haqiqiy imtihonga tayyorgarlik',
        hero_subtitle: "IELTS, SAT, Milliy sertifikat, DTM — real imtihon muhitida vaqt bilan cheklangan mashq testlari",
        hero_btn_start: 'Bepul boshlash',
        hero_btn_view: "Testlarni ko'rish",

        // Test Cards
        test_start: "Testni boshlash",
        test_badge_english: 'INGLIZ TILI',
        test_badge_academic: 'AKADEMIK',
        test_badge_national: 'MILLIY',
        test_badge_entrance: 'KIRISH',
        test_badge_cognitive: 'KOGNITIV',

        // Test Section
        tests_title: 'Testingizni tanlang',
        test_ielts_title: 'IELTS',
        test_ielts_desc: "Haqiqiy imtihon sharoitida barcha bo'limlar bo'yicha keng qamrovli IELTS amaliyoti.",
        test_sat_title: 'SAT',
        test_sat_desc: "Vaqt bilan cheklangan muhitda matematika va ingliz tili bo'limlari bilan SAT ga tayyorlaning.",
        test_milliy_title: 'Milliy sertifikat',
        test_milliy_desc: "Keng qamrovli savol bankasi bilan milliy sertifikatlash imtihoni amaliyoti.",
        test_dtm_title: 'DTM',
        test_dtm_desc: "Haqiqiy test simulyatsiyalari bilan universitet kirish imtihonlariga tayyorlaning.",

        // Features
        features_title: 'Nega UniBase?',
        feature_realistic_title: '🎯 Real imtihon muhiti',
        feature_realistic_desc: "Haqiqiy interfeys, taymer va savol formatlari bilan real imtihonlarning bosim va muhitini his qiling.",
        feature_analytics_title: "📊 Batafsil tahlil",
        feature_analytics_desc: "Kuchli va zaif tomonlaringizni, vaqt o'tishi bilan taraqqiyotingizni to'liq tahlil qilish orqali baholang.",
        feature_progress_title: "📈 Taraqqiyotni kuzatish",
        feature_progress_desc: "Dinamik taraqqiyot kuzatuvi, shaxsiy tavsiyalar va maqsad belgilash bilan yaxshilanishingizni kuzating.",

        // Login Page
        login_title: 'Xush kelibsiz',
        login_subtitle: "Imtihonga tayyorgarlikni davom ettirish uchun kiring",
        login_email: 'Email manzil',
        login_password: 'Parol',
        login_remember: "Meni eslab qol",
        login_btn: 'Kirish',
        login_no_account: "Hisobingiz yo'qmi?",
        login_register_here: "Bu yerda ro'yxatdan o'ting",
        login_demo: "Demo ma'lumotlar:",

        // Register Page
        register_title: "Hisob yaratish",
        register_subtitle: "Imtihonga tayyorgarlik sayohatingizni boshlang",
        register_name: "To'liq ism",
        register_email: 'Email manzil',
        register_student_id: "Talaba ID (ixtiyoriy)",
        register_password: 'Parol',
        register_confirm: "Parolni tasdiqlang",
        register_btn: "Hisob yaratish",
        register_have_account: "Hisobingiz bormi?",
        register_login_here: "Bu yerda kiring",

        // Student Dashboard
        dashboard_welcome: 'Xush kelibsiz',
        dashboard_subtitle: "Amaliy mashg'ulotni boshlash uchun testni tanlang",
        dashboard_available_tests: "Mavjud testlar",
        dashboard_recent_results: "Mening so'nggi natijalarim",
        dashboard_no_tests: "Hozircha testlar mavjud emas. Keyinroq tekshiring.",
        dashboard_no_results: "Siz hali test topshirmadingiz. Natijalarni ko'rish uchun mashq qilishni boshlang!",

        // Common
        duration: 'Davomiyligi',
        questions: 'Savollar',
        minutes: 'daqiqa',
        footer_rights: "Barcha huquqlar himoyalangan.",
        footer_copyright: '© 2026 UniBase. Barcha huquqlar himoyalangan.',
        footer_tests: 'Testlar',
        footer_features: 'Xususiyatlar',
        footer_privacy: 'Maxfiylik siyosati',
        footer_contact: 'Aloqa',
        home: 'Bosh sahifa',

        // Admin Dashboard
        admin_dashboard_title: 'Admin paneli',
        admin_dashboard_subtitle: "Testlarni boshqarish va talabalar faoliyatini kuzatish",
        admin_total_tests: 'Jami testlar',
        admin_registered_students: "Ro'yxatdan o'tgan talabalar",
        admin_test_attempts: 'Test urinishlari',
        admin_quick_actions: 'Tez harakatlar',
        admin_add_new_test: 'Yangi test qo\'shish',
        admin_add_test_desc: "Talabalar uchun yangi imtihon yaratish",
        admin_create_test: 'Test yaratish',
        admin_manage_tests_title: "Testlarni boshqarish",
        admin_manage_tests_desc: "Mavjud testlarni ko'rish, tahrirlash yoki o'chirish",
        admin_view_tests: "Testlarni ko'rish",
        admin_view_students_title: "Talabalarni ko'rish",
        admin_view_students_desc: "Barcha ro'yxatdan o'tgan talabalar va ularning taraqqiyotini ko'rish",
        admin_view_students_btn: "Talabalarni ko'rish",
        admin_recent_activity: "So'nggi test faoliyati",
        admin_no_activity: "Test faoliyati hali yo'q.",
        admin_registered_students_title: "Ro'yxatdan o'tgan talabalar",
        admin_no_students: "Hali talabalar ro'yxatdan o'tmagan.",

        // Admin Tests Management
        admin_tests_manage_title: "Testlarni boshqarish",
        admin_tests_add_new: "Yangi test qo'shish",
        admin_tests_create_new: 'Yangi test yaratish',
        admin_tests_edit: 'Testni tahrirlash',
        admin_tests_test_name: 'Test nomi',
        admin_tests_category: 'Kategoriya',
        admin_tests_select_category: 'Kategoriyani tanlang...',
        admin_tests_duration_min: 'Davomiyligi (daqiqa)',
        admin_tests_description: 'Tavsif',
        admin_tests_questions_section: 'Savollar',
        admin_tests_add_question: "Savol qo'shish",
        admin_tests_save: 'Testni saqlash',
        admin_tests_cancel: 'Bekor qilish',
        admin_tests_existing: 'Mavjud testlar',
        admin_tests_no_tests: "Testlar hali yaratilmagan. Yaratish uchun \"Yangi test qo'shish\" tugmasini bosing.",
        admin_tests_edit_btn: 'Tahrirlash',
        admin_tests_delete_btn: "O'chirish",
        admin_tests_created: 'Yaratilgan',
        admin_tests_question_text: 'Savol matni',
        admin_tests_option: 'Variant',
        admin_tests_correct_answer: "To'g'ri javob",
        admin_tests_select_correct: "To'g'ri javobni tanlang...",
        admin_tests_remove: "O'chirish",
        admin_tests_question: 'Savol',

        // Test Taking
        test_taking_loading: 'Test yuklanmoqda...',
        test_taking_question_of: 'Savol',
        test_taking_of: 'dan',
        test_taking_pause: 'Pauza',
        test_taking_resume: 'Davom ettirish',
        test_taking_previous: 'Oldingi',
        test_taking_next: 'Keyingi',
        test_taking_submit: "Testni topshirish",

        // Test Results
        results_title: 'Test natijalari',
        results_your_score: 'Sizning natijangiz',
        results_percentage: 'Foiz',
        results_time_taken: 'Sarflangan vaqt',
        results_answer_review: "Javoblarni ko'rib chiqish",
        results_back_dashboard: 'Panelga qaytish',
        results_print: "Natijalarni chop etish",
        results_excellent: 'Ajoyib!',
        results_excellent_msg: "A'lo natija!",
        results_good: "Yaxshi ish!",
        results_good_msg: 'Siz testdan o\'tdingiz.',
        results_fair: "Yaxshi",
        results_fair_msg: "Materialni ko'rib chiqishni va qayta urinib ko'rishni o'ylab ko'ring.",
        results_keep_practicing: "Mashq qilishda davom eting",
        results_practice_msg: "Materialni ko'rib chiqing va qayta urinib ko'ring.",
        results_correct: "To'g'ri",
        results_incorrect: "Noto'g'ri",
        results_your_answer: 'Sizning javobingiz',
        results_correct_answer: "To'g'ri javob",
        results_not_answered: 'Javob berilmagan',

        // Table Headers
        table_name: 'Ism',
        table_email: 'Email',
        table_student_id: 'Talaba ID',
        table_registered: "Ro'yxatdan o'tgan",
        table_student: 'Talaba',
        table_test: 'Test',
        table_test_name: 'Test nomi',
        table_score: 'Natija',
        table_time: 'Vaqt',
        table_date: 'Sana',
    }
};

// Get saved language or default to English
function getCurrentLanguage() {
    return localStorage.getItem('unibase_language') || 'en';
}

// Set language
function setLanguage(lang) {
    localStorage.setItem('unibase_language', lang);
    applyTranslations(lang);
}

// Apply translations to the page
function applyTranslations(lang) {
    const translations = TRANSLATIONS[lang] || TRANSLATIONS.en;

    // Find all elements with data-translate attribute
    document.querySelectorAll('[data-translate]').forEach(element => {
        const key = element.getAttribute('data-translate');
        if (translations[key]) {
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                element.placeholder = translations[key];
            } else {
                element.textContent = translations[key];
            }
        }
    });

    // Update language selector
    const langSelector = document.getElementById('language-selector');
    if (langSelector) {
        langSelector.value = lang;
    }
}

// Initialize language on page load
document.addEventListener('DOMContentLoaded', function () {
    const currentLang = getCurrentLanguage();
    applyTranslations(currentLang);

    // Language selector change event
    const langSelector = document.getElementById('language-selector');
    if (langSelector) {
        langSelector.value = currentLang;
        langSelector.addEventListener('change', function () {
            setLanguage(this.value);
        });
    }
});
