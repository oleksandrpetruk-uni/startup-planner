# Лабораторна робота: Моделювання вимог

**Проєкт:** Startup Planner
**Виконав:** Петрук Олександр

## Крок 1. Обрати проєкт
**Опис:** Startup Planner - веб-сервіс, який допомагає творцям стартапів сфокусуватися на одній цільовій аудиторії, зрозуміти свою найбільшу проблему та автоматично скласти чіткий план дій на тиждень.

## Крок 2. Функціональні вимоги (FR)
* **FR-01:** Користувач повинен мати можливість вибрати лише одну головну аудиторію (заборона множинного вибору).
* **FR-02:** На сайті має бути текстове поле для опису найбільшої проблеми користувача (Blocker).
* **FR-03:** Система повинна аналізувати введену проблему і показувати можливі ризики.
* **FR-04:** Система повинна автоматично генерувати готовий покроковий план завдань на найближчі 7 днів.
* **FR-05:** На головній сторінці має бути вікно для введення email, щоб підписатися на оновлення.
* **FR-06:** Система має автоматично перевіряти, чи правильно людина ввела email (наявність символу "@").

## Крок 3. Діаграма прецедентів (Use Case Diagram)
```mermaid
flowchart LR
    User(["Користувач (Фаундер)"])
    MailAPI(["Поштовий сервіс (API)"])

    subgraph "Система Startup Planner"
        UC1([Вибрати цільову аудиторію])
        UC2([Описати проблему / Blocker])
        UC3([Отримати аналіз ризиків])
        UC4([Отримати план на 7 днів])
        UC5([Підписатися на Waitlist])
        UC6([Валідувати формат email])
    end

    User --- UC1
    User --- UC2
    User --- UC5

    UC2 -. "<<include>>" .-> UC3
    UC3 -. "<<include>>" .-> UC4
    UC5 -. "<<include>>" .-> UC6

    UC5 --- MailAPI
```

## Крок 4. Діаграма класів (Class Diagram)
```mermaid
classDiagram
    class UserSession {
        +String sessionId
        +String email
        +startSession()
        +subscribeToWaitlist(email: String)
    }

    class TargetAudience {
        +String audienceName
        +boolean isSelected
        +selectSingleAudience()
    }

    class BlockerAnalyzer {
        +String problemText
        +List~String~ risks
        +analyzeProblem(text: String)
    }

    class ActionPlan {
        +Date creationDate
        +String status
        +generateSevenDayPlan(risks: List)
    }
    
    class PdfActionPlan {
        +String pdfFormatUrl
        +downloadAsPdf()
    }

    class Task {
        +int dayNumber
        +String description
        +boolean isCompleted
        +markAsDone()
    }

    UserSession "1" --> "1" TargetAudience : обирає
    UserSession "1" --> "1" BlockerAnalyzer : вводить дані
    BlockerAnalyzer "1" --> "1" ActionPlan : ініціює генерацію
    ActionPlan "1" *-- "7..*" Task : складається з
    ActionPlan <|-- PdfActionPlan : Наслідування
```

## Крок 5. Діаграма послідовності (Sequence Diagram)
```mermaid
sequenceDiagram
    actor User as Користувач
    participant UI as Інтерфейс (Frontend)
    participant Analyzer as BlockerAnalyzer
    participant Generator as ActionPlan (Генератор)

    User->>UI: Вводить опис проблеми та натискає "Далі"
    activate UI
    
    UI->>Analyzer: analyzeProblem(problemText)
    activate Analyzer
    
    alt Якщо тексту достатньо (валідні дані)
        Analyzer-->>UI: return risksList
        
        UI->>Generator: generateSevenDayPlan(risksList)
        activate Generator
        Generator-->>UI: return 7DaysTasks
        deactivate Generator
        
        UI-->>User: Відображає ризики та готовий план
    else Якщо текст занадто короткий
        Analyzer-->>UI: return Error("Опишіть проблему детальніше")
        UI-->>User: Показує попередження
    end
    
    deactivate Analyzer
    deactivate UI
```

## Крок 6. Матриця трасовності (Traceability Matrix)

| Ідентифікатор вимоги (FR) | Прецедент (Use Case) | Задіяні класи (Classes) | Діаграма послідовності |
| :--- | :--- | :--- | :--- |
| **FR-01** | UC1 (Вибрати цільову аудиторію) | `UserSession`, `TargetAudience` | Ні |
| **FR-02** | UC2 (Описати проблему) | `UserSession`, `BlockerAnalyzer` | Так |
| **FR-03** | UC3 (Отримати аналіз ризиків) | `BlockerAnalyzer` | Так |
| **FR-04** | UC4 (Отримати план на 7 днів) | `ActionPlan`, `Task` | Так |
| **FR-05** | UC5 (Підписатися на Waitlist) | `UserSession` | Ні |
| **FR-06** | UC6 (Валідувати формат email) | `UserSession` | Ні |
