# Quiz Application - System Architecture

## Application Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     QUIZ APPLICATION                         │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
                   ┌───────────────┐
                   │  Landing Page │
                   │   (Login)     │
                   └───────┬───────┘
                           │
               ┌───────────┴───────────┐
               ▼                       ▼
       ┌──────────────┐        ┌──────────────┐
       │  Register    │        │   Login      │
       │  (New User)  │        │  (Existing)  │
       └──────┬───────┘        └──────┬───────┘
              │                       │
       ┌──────┴──────┐               │
       ▼             ▼               │
   ┌───────┐    ┌────────┐          │
   │ Admin │    │Student │          │
   └───┬───┘    └───┬────┘          │
       │            │               │
       └────────────┴───────────────┘
                    │
           ┌────────┴────────┐
           ▼                 ▼
   ┌──────────────┐  ┌──────────────┐
   │    Admin     │  │   Student    │
   │  Dashboard   │  │  Dashboard   │
   └──────┬───────┘  └──────┬───────┘
          │                 │
          │                 │
   ┌──────┴──────┐   ┌──────┴──────┐
   ▼             ▼   ▼             ▼
┌────────┐  ┌──────────┐ ┌──────┐ ┌──────┐
│ Create │  │   View   │ │ Take │ │ View │
│  Quiz  │  │ Results  │ │ Quiz │ │History│
└────┬───┘  └─────┬────┘ └──┬───┘ └──────┘
     │            │          │
     ▼            │          ▼
┌─────────┐       │     ┌─────────┐
│   Add   │       │     │ Submit  │
│Questions│       │     │  Quiz   │
└─────────┘       │     └────┬────┘
                  │          │
                  │          ▼
                  │     ┌─────────┐
                  │     │  View   │
                  │     │ Results │
                  │     └─────────┘
                  │
                  ▼
        ┌──────────────────┐
        │  Export Results  │
        │  (Excel / PDF)   │
        └──────────────────┘
                  │
                  ▼
        ┌──────────────────┐
        │  Export Questions│
        │  (PDF / DOCX)    │
        └──────────────────┘
```

## Database Schema

```
┌────────────────────────────────────────────────────────────┐
│                      DATABASE SCHEMA                        │
└────────────────────────────────────────────────────────────┘

┌─────────────┐
│    User     │
├─────────────┤
│ id          │◄──────────┐
│ username    │           │
│ email       │           │
│ phone       │           │
│ password    │           │
│ role        │           │
│ roll_number │           │
│ branch      │           │
└─────────────┘           │
      │                  │
      │                  │
      │ created_by       │
      │                  │
      ▼                  │
┌─────────────┐           │
│    Quiz     │           │
├─────────────┤           │
│ id          │◄──┐       │
│ title       │   │       │
│ description │   │       │
│ time_limit  │   │       │
│ is_active   │   │       │
│ created_by  │───┘       │
└─────────────┘           │
      │                  │
      │ quiz             │
      │                  │
      ▼                  │
┌─────────────┐           │
│  Question   │           │
├─────────────┤           │
│ id          │◄──┐       │
│ quiz_id     │   │       │
│ question    │   │       │
│ option_a    │   │       │
│ option_b    │   │       │
│ option_c    │   │       │
│ option_d    │   │       │
│ correct_ans │   │       │
│ marks       │   │       │
│ order       │   │       │
└─────────────┘   │       │
                 │       │
      ┌──────────┘       │
      │                  │
      │ student          │
      │                  │
      ▼                  │
┌─────────────┐           │
│QuizAttempt  │           │
├─────────────┤           │
│ id          │◄──┐       │
│ student_id  │───┼───────┘
│ quiz_id     │   │
│ score       │   │
│ total_marks │   │
│ is_completed│   │
│ started_at  │   │
│ completed_at│   │
│question_order│  │
└─────────────┘   │
                 │
      │ attempt  │
      │          │
      ▼          │
┌─────────────┐   │
│StudentAnswer│   │
├─────────────┤   │
│ id          │   │
│ attempt_id  │───┘
│ question_id │
│ selected_ans│
│ is_correct  │
└─────────────┘
```

## User Flow - Admin

```
1. Register/Login
   └─► Enter captcha
        └─► Authenticate
             └─► Admin Dashboard

2. Create Quiz
   └─► Enter title, description, time limit
        └─► Save quiz
             └─► Add Questions

3. Add Questions
   └─► Enter question text
        └─► Enter 4 options (A, B, C, D)
             └─► Select correct answer
                  └─► Set marks
                       └─► Save
                            └─► Add more or finish

4. View Results
   └─► Select quiz
        └─► View student attempts
             └─► Download Excel/PDF

5. Export Questions
   └─► Select quiz
        └─► Export to PDF/DOCX
```

## User Flow - Student

```
1. Register/Login
   └─► Enter captcha
        └─► Authenticate
             └─► Student Dashboard

2. Browse Quizzes
   └─► View available quizzes
        └─► Select quiz
             └─► Start attempt

3. Take Quiz
   └─► Timer starts
        └─► Questions in shuffled order
             └─► Answer questions
                  └─► Navigate (Next/Previous)
                       └─► Exit with confirmation
                            └─► Submit
                                 └─► View results

4. View Results
   └─► See score
        └─► Review answers
             └─► Check correct answers
```

## Component Architecture

```
┌────────────────────────────────────────────────────────────┐
│                   DJANGO APPLICATION                        │
└────────────────────────────────────────────────────────────┘

┌───────────────┐
│   Browser     │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│  Templates    │◄─── HTML/CSS/JS
│  (Frontend)   │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│     URLs      │◄─── Route requests
│   (Routing)   │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│    Views      │◄─── Business logic
│  (Controller) │
└───────┬───────┘
        │
        ├──────────────────┐
        ▼                  ▼
┌───────────────┐  ┌───────────────┐
│    Forms      │  │    Models     │
│ (Validation)  │  │  (Database)   │
└───────────────┘  └───────┬───────┘
                           │
                           ▼
                   ┌───────────────┐
                   │  PostgreSQL   │
                   │   Database    │
                   └───────────────┘
```

## Security Flow

```
┌─────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                       │
└─────────────────────────────────────────────────────────┘

User Input
    │
    ▼
┌─────────────┐
│   CSRF      │  Token validation
│ Protection  │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│   Captcha   │  6-digit validation
│ Validation  │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│   Django    │  User authentication
│    Auth     │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│  Password   │  PBKDF2 hashing
│   Hashing   │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│    Role     │  Admin/Student check
│   Check     │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│   Access    │  View permissions
│   Control   │
└─────────────┘
```

## Quiz Taking Flow

```
Start Quiz
    │
    ▼
┌─────────────┐
│ Check if    │──► Already attempted? → Error
│ attempted   │
└─────┬───────┘
      │ No
      ▼
┌─────────────┐
│   Create    │
│  Attempt    │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ Start Timer │
└─────┬───────┘
      │
      ▼
┌─────────────────────┐
│ Shuffle Questions   │
│ Store order in DB   │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Display Question   │◄───┐
│                     │    │
│  [A] Option A      │    │
│  [B] Option B      │    │
│  [C] Option C      │    │
│  [D] Option D      │    │
│                     │    │
│ [Prev] [Clear] [Next]│───┘
│        [Exit]       │
└─────────┬───────────┘
          │
    ┌─────┴─────┐
    ▼           ▼
┌─────────┐ ┌──────────┐
│  Exit   │ │  Submit  │
└────┬────┘ └────┬─────┘
     │           │
     ▼           ▼
┌─────────┐ ┌────────────────┐
│Confirm  │ │ Calculate Score│
│ Exit    │ │ Save Answers   │
└────┬────┘ └────────┬───────┘
     │No         Yes│
     │              ▼
     │       ┌────────────────┐
     │       │ Display Results│
     │       └────────────────┘
     ▼
┌─────────────────────┐
│ Continue Quiz       │
└─────────────────────┘
```

## Export Flow

```
Admin clicks Export
        │
        ▼
┌────────────────┐
│  Select Type   │
└────────┬───────┘
         │
    ┌────┴────┐
    ▼         ▼
┌─────────┐ ┌─────────────┐
│Results  │ │  Questions  │
└────┬────┘ └──────┬──────┘
     │             │
     ▼             ▼
┌────────────────┐ ┌────────────────┐
│ Select Format  │ │ Select Format  │
└────────┬───────┘ └────────┬───────┘
         │                  │
    ┌────┴────┐        ┌────┴────┐
    ▼         ▼        ▼         ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│ Excel │ │  PDF  │ │  PDF  │ │ DOCX  │
└───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘
    │         │         │         │
    └─────────┼─────────┼─────────┘
              │         │
              ▼         ▼
    ┌─────────────────────────┐
    │    Fetch Data from      │
    │       Database          │
    └──────────┬──────────────┘
               │
               ▼
    ┌─────────────────────────┐
    │      Format Data        │
    │ - Student name          │
    │ - Roll number           │
    │ - Score                 │
    │ - Percentage            │
    │ - Questions & Options   │
    │ - Correct Answers       │
    └──────────┬──────────────┘
               │
               ▼
    ┌─────────────────────────┐
    │     Generate File       │
    │      with Styling       │
    └──────────┬──────────────┘
               │
               ▼
    ┌─────────────────────────┐
    │        Download         │
    └─────────────────────────┘
```

## Session Flow

```
Login Success
     │
     ▼
┌──────────────┐
│Create Session│
│  - user_id   │
│  - role      │
│  - captcha   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Set Cookie   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Redirect to  │
│  Dashboard   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Each Request │
│ Validated    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Logout     │
│ Clear Session│
└──────────────┘
```

---

**Legend:**
- `│` : Flow direction
- `▼` : Next step
- `◄─` : Relationship
- `┌─┐` : Component/Process
- `└─┘` : End of component