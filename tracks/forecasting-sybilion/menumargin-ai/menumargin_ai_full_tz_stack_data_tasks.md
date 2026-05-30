# MenuMargin AI — Full Hackathon ТЗ
## Restaurant Ingredient Forecasting → Dish Margin Protection Agent

**Track:** Forecasting AI  
**Project:** MenuMargin AI  
**Goal:** построить decision agent, который прогнозирует себестоимость ингредиентов ресторана на 6 месяцев, пересчитывает себестоимость блюд и рекомендует действия, чтобы маржа блюд не падала ниже target margin.

---

# 0. Короткая суть проекта

**MenuMargin AI** — это decision-support система для ресторанов.

Ресторан загружает:

1. историю цен ингредиентов за 5 лет;
2. рецепты блюд;
3. текущие цены меню;
4. target margin;
5. ограничения бизнеса.

Система:

1. берёт monthly time series по каждому ингредиенту;
2. отправляет данные в Sybilion Forecasting API;
3. получает forecast на 6 месяцев;
4. считает будущую себестоимость каждого блюда;
5. считает будущую маржу каждого блюда;
6. находит блюда с риском падения маржи;
7. рекомендует:
   - поднять цену;
   - поднять цену постепенно;
   - купить ингредиенты заранее;
   - изменить рецепт;
   - принять временное падение маржи;
   - отправить на manual review;
8. показывает reasoning;
9. адаптируется при изменении assumptions во время live demo.

---

# 1. Главная формула проекта

```text
Ingredient price history
    ↓
Sybilion Forecasting API
    ↓
Ingredient cost forecast
    ↓
Dish cost forecast
    ↓
Margin risk detection
    ↓
Recommendation engine
    ↓
Scenario adaptation
```

---

# 2. One-liner для pitch

> MenuMargin AI helps restaurants protect dish margins by forecasting ingredient costs and recommending price, recipe, and procurement actions before margins collapse.

---

# 3. Почему это подходит под трек Forecasting AI

Вам не нужно строить свою forecasting model. Forecasting engine уже даёт Sybilion API. Ваша ценность — в слое поверх прогноза:

- data preparation;
- API integration;
- dish-level aggregation;
- margin risk logic;
- recommendation engine;
- scenario adaptation;
- visible reasoning.

Это не dashboard. Это decision agent.

---

# 4. MVP Scope

## 4.1. Demo restaurant

```text
Italian Bistro
```

## 4.2. MVP dishes

```text
1. Margherita Pizza
2. Pasta Pomodoro
3. Carbonara
```

## 4.3. MVP ingredients

```text
1. pasta
2. tomatoes
3. cheese / mozzarella proxy
4. olive oil
5. eggs
6. flour
7. beef/chicken optional
```

## 4.4. Forecast horizon

```text
6 months
```

Для 6-месячного горизонта нужно минимум 60 monthly data points. Поэтому берём историю с 2020-01 или раньше.

---

# 5. Stack

## 5.1. Backend

```text
Python
FastAPI
Pydantic
Pandas
NumPy
httpx / requests
SQLite or JSON cache
```

### Почему

FastAPI быстро даёт endpoints, Pydantic валидирует payload, Pandas нужен для обработки CSV и time series. SQLite/JSON cache нужен не ради production, а чтобы demo не умерло, если API решит устроить драму.

---

## 5.2. Frontend

```text
React / Next.js
TypeScript
TailwindCSS
Recharts or Plotly
```

### Почему

Нужен один быстрый dashboard:

- summary cards;
- menu risk table;
- ingredient forecast chart;
- dish margin chart;
- recommendation card;
- scenario controls;
- reasoning panel.

---

## 5.3. Data stack

```text
Eurostat REST API
World Bank Pink Sheet XLSX
ECB exchange rate API
Manual current price anchors
CSV files
Pandas processing scripts
```

---

## 5.4. Forecasting

```text
Sybilion Forecasting API
```

---

## 5.5. Optional LLM

```text
Gemini / OpenAI / Claude
```

Только для красивой переформулировки reasoning. Decision должен идти из deterministic engine, а не из “AI said so”, потому что это любимый жанр людей, которые строят туман вместо архитектуры.

---

# 6. Что НЕ делать

Не тратить время на:

```text
auth
payments
multi-tenant restaurants
full POS integration
database-heavy architecture
mobile app
microservices
real production deployment
advanced ML model
complex supplier marketplace
```

---

# 7. Data Sources

## 7.1. Primary source: Eurostat HICP

### Dataset

```text
prc_hicp_midx
```

### Type

```text
HICP monthly index, 2015=100
```

### UI

```text
https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_midx/default/table?lang=en
```

### REST API base

```text
https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_midx
```

### Example API

```text
https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_midx?format=CSV&geo=EU27_2020&sinceTimePeriod=2020-01&coicop=CP01121&coicop=CP01124&coicop=CP01153&coicop=CP01171&coicop=CP01144
```

### Parameters

```text
format=CSV or JSON
geo=EU27_2020
sinceTimePeriod=2020-01
coicop=COICOP_CODE
```

### Use

Eurostat HICP gives index, not €/kg.

So we reconstruct historical prices:

```text
price_t = current_price_per_kg * (index_t / index_today)
```

### Source type

```text
index_reconstructed
```

---

## 7.2. Eurostat COICOP mapping

| Ingredient | COICOP code | Description |
|---|---|---|
| Beef | CP01121 | Beef and veal |
| Pork | CP01122 | Pork |
| Chicken | CP01124 | Poultry |
| Lamb | CP01123 | Lamb and goat |
| Fish general | CP0113 | Fish and seafood |
| Fresh fish | CP01131 | Fresh/chilled fish |
| Milk | CP01141 | Fresh whole milk |
| Cheese | CP01144 | Cheese and curd |
| Eggs | CP01147 | Eggs |
| Butter | CP01151 | Butter |
| Olive oil | CP01153 | Olive oil |
| Other oils | CP01154 | Other edible oils |
| Fresh fruit | CP01161 | Fresh/chilled fruit |
| Fresh vegetables | CP01171 | Fresh/chilled vegetables |
| Potatoes | CP01174 | Potatoes |
| Flour/cereals | CP01112 | Flours and other cereals |
| Bread | CP01113 | Bread |
| Pasta | CP01116 | Pasta products and couscous |
| Rice | CP01111 | Rice |
| Sugar | CP01181 | Sugar |
| Coffee | CP0121 | Coffee, tea and cocoa |
| Chocolate | CP01183 | Chocolate |

---

## 7.3. Secondary source: World Bank Pink Sheet

### Monthly Excel

```text
https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx
```

### Coverage

```text
1960 → May 2026
monthly
```

### Includes

```text
wheat
maize
rice
sugar
beef
chicken
lamb
shrimp
salmon
olive oil
soybean oil
sunflower oil
coffee
cocoa
tea
orange
banana
```

### Units

Usually:

```text
USD/kg
USD/mt
USD/unit
```

Need conversion to EUR.

---

## 7.4. ECB EUR/USD exchange rate

### API

```text
https://data-api.ecb.europa.eu/service/data/EXR/M.USD.EUR.SP00.A?format=csvdata
```

### Use

For World Bank data:

```text
USD price → EUR price
```

---

## 7.5. FAO FPMA Tool

### UI

```text
https://fpma.fao.org/giews/fpmat4/#/dashboard/home
```

### Use

Domestic retail/wholesale food prices.

### Problem

Western EU coverage may be weak.

### Priority

Fallback / sanity check.

---

## 7.6. FAOSTAT Producer Prices

```text
https://www.fao.org/faostat/en/#data/PP
```

Use:

```text
Europe → All items → Monthly → Download CSV
```

Could be useful, but not P0.

---

## 7.7. FAOSTAT Food CPI

```text
https://www.fao.org/faostat/en/#data/CP
```

Use as macro proxy if needed.

---

## 7.8. EU Agri-food Price Dashboard

### Dashboard

```text
https://agriculture.ec.europa.eu/data-and-analysis/markets/price-dashboard_en
```

### Includes

```text
beef carcass
pork carcass
poultry
raw milk
butter
cheese
wheat
barley
maize
olive oil
sugar
```

### Units

```text
€/100kg
€/tonne
```

### Problem

Often PDF/dashboard-first, no easy API.

### Use

Only if quick CSV/table extraction works.

---

## 7.9. Eurostat Agricultural Prices

### Dataset

```text
apri_pi00_outa
```

### UI

```text
https://ec.europa.eu/eurostat/databrowser/view/apri_pi00_outa/default/table?lang=en
```

### Use

Actual producer prices for agricultural products.

### Priority

P1, not P0.

Use only after Eurostat HICP is working.

---

## 7.10. FRED mirror

### Example

```text
https://api.stlouisfed.org/fred/series/observations?series_id=CP0110EZ19M086NEST&api_key=YOUR_KEY&file_type=json
```

### Problem

Requires API key.

### Priority

Low. Only if Eurostat JSON-stat becomes annoying.

---

# 8. Data Strategy

## 8.1. Main strategy

Use:

```text
Eurostat HICP index
+ current price anchors
+ reconstruction formula
```

Final output:

```csv
ingredient,date,price_per_kg,source,source_type,proxy_category,geo
```

## 8.2. Why not exact restaurant wholesale data

Exact restaurant procurement prices are hard to get in 36 hours. Instead use official European food price indices and reconstruct approximate ingredient cost history.

This is honest and reproducible.

---

# 9. Current Price Anchors

## 9.1. Purpose

Eurostat gives index, not €/kg. We need current price per kg to reconstruct historical €/kg.

## 9.2. How to get current prices

Fast method:

- manually check Billa / REWE / Spar / Hofer;
- use average estimates;
- write source clearly;
- do not waste time scraping.

## 9.3. File

```text
data/current_prices.csv
```

## 9.4. Example

```csv
ingredient,current_price_per_kg,source,note
pasta,2.20,manual_benchmark,average supermarket price
tomatoes,3.49,manual_benchmark,average supermarket price
cheese,9.90,manual_benchmark,cheese proxy
olive_oil,11.50,manual_benchmark,converted from liter to kg approx
eggs,5.00,manual_benchmark,converted to kg estimate
flour,1.40,manual_benchmark,average supermarket price
```

---

# 10. Reconstruction Method

## 10.1. Formula

```text
historical_price_t = current_price_per_kg * index_t / latest_index
```

## 10.2. Example

```text
current olive oil price = 11.50 €/kg
latest index = 150
2020-01 index = 100

historical price 2020-01 = 11.50 * 100 / 150 = 7.67 €/kg
```

## 10.3. Output

```csv
ingredient,date,price_per_kg,index_value,current_price_per_kg,latest_index,source,source_type,proxy_category
olive_oil,2020-01,7.67,100.0,11.50,150.0,Eurostat,index_reconstructed,CP01153
```

---

# 11. Final Data Files

## 11.1. Source config

```text
data/config/ingredient_sources.csv
```

```csv
ingredient,source,coicop,geo,source_type,proxy_description
pasta,Eurostat,CP01116,EU27_2020,index_reconstructed,Pasta products and couscous
tomatoes,Eurostat,CP01171,EU27_2020,index_reconstructed,Fresh vegetables proxy
cheese,Eurostat,CP01144,EU27_2020,index_reconstructed,Cheese and curd
olive_oil,Eurostat,CP01153,EU27_2020,index_reconstructed,Olive oil
eggs,Eurostat,CP01147,EU27_2020,index_reconstructed,Eggs
flour,Eurostat,CP01112,EU27_2020,index_reconstructed,Flours and cereals
```

## 11.2. Current prices

```text
data/current_prices.csv
```

## 11.3. Raw index output

```text
data/raw/eurostat_hicp.csv
```

## 11.4. Processed ingredient prices

```text
data/processed/ingredient_prices.csv
```

Final schema:

```csv
ingredient,date,price_per_kg,index_value,current_price_per_kg,latest_index,source,source_type,proxy_category,geo,confidence
```

## 11.5. Recipes

```text
data/demo/recipes.csv
```

```csv
dish,ingredient,grams
Margherita Pizza,tomatoes,120
Margherita Pizza,cheese,100
Margherita Pizza,flour,180
Margherita Pizza,olive_oil,10
Pasta Pomodoro,pasta,140
Pasta Pomodoro,tomatoes,160
Pasta Pomodoro,olive_oil,12
Carbonara,pasta,130
Carbonara,cheese,30
Carbonara,eggs,60
```

## 11.6. Menu

```text
data/demo/menu.csv
```

```csv
dish,current_price,target_margin
Margherita Pizza,12.90,0.65
Pasta Pomodoro,11.90,0.64
Carbonara,14.50,0.65
```

---

# 12. Task Breakdown

We split the project into 8 workstreams:

```text
1. Data research and source mapping
2. Data extraction and reconstruction
3. Sybilion API integration
4. Ingredient forecast processing
5. Dish cost and margin engine
6. Recommendation engine
7. Scenario engine
8. Frontend and demo
```

---

# BLOCK 1 — Data Research and Source Mapping

## Owner

Data person

## Goal

Find usable ingredient/category mappings and confirm source availability.

## Tasks

### 1.1. Choose final MVP ingredients

Recommended:

```text
pasta
tomatoes
cheese
olive_oil
eggs
flour
```

### 1.2. Map ingredients to Eurostat COICOP codes

Use:

```text
CP01116 pasta
CP01171 vegetables/tomatoes proxy
CP01144 cheese
CP01153 olive oil
CP01147 eggs
CP01112 flour/cereals
```

### 1.3. Decide geography

Priority:

```text
EU27_2020 first
AT if available and fast
```

### 1.4. Create source config CSV

Output:

```text
data/config/ingredient_sources.csv
```

### 1.5. Check data availability

For each COICOP:

- run API request;
- check monthly points;
- ensure 60+ observations;
- save quick notes.

## Deliverables

```text
ingredient_sources.csv
data_availability_notes.md
```

---

# BLOCK 2 — Data Extraction and Reconstruction

## Owner

Data engineer

## Goal

Build final ingredient_prices.csv.

## Tasks

### 2.1. Create Eurostat fetch script

File:

```text
scripts/fetch_eurostat_hicp.py
```

Responsibilities:

- read `ingredient_sources.csv`;
- call Eurostat REST API;
- fetch CSV/JSON;
- save raw data.

### 2.2. Save raw Eurostat output

Folder:

```text
data/raw/
```

Output:

```text
eurostat_hicp_raw.csv
```

### 2.3. Create current price anchors

File:

```text
data/current_prices.csv
```

Use manual benchmark prices.

### 2.4. Create reconstruction script

File:

```text
scripts/reconstruct_ingredient_prices.py
```

Responsibilities:

- load HICP index data;
- load current prices;
- find latest index per ingredient;
- apply formula;
- produce monthly €/kg history.

### 2.5. Validate data

Rules:

```text
each ingredient >= 60 rows
date format YYYY-MM
no negative prices
no huge missing gaps
same date range if possible
```

### 2.6. Create validation report

Output:

```text
data/processed/validation_report.json
```

## Deliverables

```text
data/processed/ingredient_prices.csv
data/processed/validation_report.json
```

---

# BLOCK 3 — Sybilion API Integration

## Owner

Backend / API person

## Goal

Send ingredient time series to Sybilion API and receive forecast.

## Tasks

### 3.1. Read Sybilion API docs

Output:

```text
docs/sybilion_api_notes.md
```

Must document:

- endpoint;
- auth;
- request format;
- response format;
- quota;
- required fields.

### 3.2. Create Sybilion client

File:

```text
backend/app/services/sybilion_client.py
```

Main function:

```python
run_forecast(
    ingredient_name: str,
    time_series: list[dict],
    keywords: list[str],
    horizon_months: int = 6
)
```

### 3.3. Create ingredient keywords config

File:

```text
data/config/ingredient_keywords.json
```

Example:

```json
{
  "olive_oil": [
    "olive oil price",
    "mediterranean drought",
    "spain olive production",
    "energy costs",
    "transport costs"
  ],
  "cheese": [
    "cheese price",
    "milk price",
    "dairy production",
    "feed costs",
    "energy costs"
  ],
  "pasta": [
    "pasta price",
    "wheat price",
    "grain harvest",
    "fertilizer prices",
    "energy costs"
  ]
}
```

### 3.4. Run first API call

Start with:

```text
olive_oil
```

because it has a clean COICOP code and strong narrative.

### 3.5. Save successful response

Output:

```text
data/cache/olive_oil_forecast_raw.json
```

### 3.6. Create mock fallback

Output:

```text
data/mock/sybilion_forecast_mock.json
```

This is mandatory for demo safety.

## Deliverables

```text
sybilion_client.py
ingredient_keywords.json
first_forecast_response.json
mock_forecast_response.json
```

---

# BLOCK 4 — Ingredient Forecast Processing

## Owner

Backend/data person

## Goal

Normalize ingredient forecasts into one consistent format.

## Tasks

### 4.1. Create forecast normalizer

File:

```text
backend/app/services/forecast_normalizer.py
```

Output format:

```json
{
  "ingredient": "olive_oil",
  "current_price_per_kg": 11.50,
  "forecast": [
    {
      "month": "2026-06",
      "median": 11.90,
      "lower_band": 10.80,
      "upper_band": 13.40
    }
  ],
  "drivers": [
    {
      "month": "2026-06",
      "driver": "drought conditions",
      "importance": 0.32
    }
  ],
  "backtest": {
    "mape": 0.06,
    "reliability": "medium"
  }
}
```

### 4.2. Run forecast for all ingredients

Input:

```text
ingredient_prices.csv
```

Output:

```text
data/cache/all_ingredient_forecasts.json
```

### 4.3. Calculate ingredient risk metrics

For each ingredient:

```text
band_width = upper_band - lower_band
band_width_pct = band_width / median
upside_risk = (upper_band - current_price) / current_price
trend_pct = (median_month_6 - current_price) / current_price
```

### 4.4. Identify risky ingredients

Output:

```json
{
  "highest_risk_ingredient": "olive_oil",
  "top_risky_ingredients": ["olive_oil", "cheese", "eggs"]
}
```

## Deliverables

```text
forecast_normalizer.py
all_ingredient_forecasts.json
ingredient_risk_metrics.json
```

---

# BLOCK 5 — Dish Cost and Margin Engine

## Owner

Backend logic person

## Goal

Convert ingredient forecasts into dish-level cost and margin forecasts.

## Tasks

### 5.1. Create dish cost engine

File:

```text
backend/app/services/dish_cost_engine.py
```

### 5.2. Calculate current dish cost

Formula:

```text
ingredient_cost = price_per_kg * grams / 1000
dish_cost = sum(ingredient_costs)
```

### 5.3. Calculate current margin

Formula:

```text
margin = (current_price - dish_cost) / current_price
```

### 5.4. Calculate future dish cost

For each future month:

```text
future_dish_cost[month] =
sum(forecast_ingredient_price[month] * grams / 1000)
```

### 5.5. Calculate expected/worst/best margins

```text
expected_margin = (price - median_cost) / price
worst_case_margin = (price - upper_band_cost) / price
best_case_margin = (price - lower_band_cost) / price
```

### 5.6. Detect margin risk

Risk logic:

```text
expected_margin below target → high risk
worst_case_margin below target → medium/high risk
both below target → critical
```

### 5.7. Create menu analysis endpoint

Endpoint:

```text
POST /api/menu/analyze
```

Response:

```json
{
  "summary": {
    "dishes_at_risk": 3,
    "critical_dishes": 1,
    "average_margin_drop": -0.084,
    "highest_risk_ingredient": "olive_oil"
  },
  "dishes": []
}
```

## Deliverables

```text
dish_cost_engine.py
margin_engine.py
/api/menu/analyze
menu_analysis_response.json
```

---

# BLOCK 6 — Recommendation Engine

## Owner

Backend/product logic person

## Goal

Generate business actions for each dish.

## Tasks

### 6.1. Define action types

```text
KEEP_PRICE
RAISE_PRICE_NOW
RAISE_PRICE_GRADUALLY
BUY_INGREDIENT_STOCK
CHANGE_RECIPE
ACCEPT_TEMPORARY_MARGIN_DROP
MANUAL_REVIEW
```

### 6.2. Price recommendation formula

```text
required_price = forecasted_dish_cost / (1 - target_margin)
```

### 6.3. Add price rounding

Use:

```text
round to .50 or .90
```

Example:

```text
16.73 → 16.90
```

### 6.4. Add gradual price increase plan

If price increase is too high:

```text
split across months
```

Example:

```text
14.50 → 15.30 → 16.10 → 16.90
```

### 6.5. Add procurement action

If ingredient has:

```text
high upside risk
high usage across multiple dishes
acceptable storage
```

Recommend:

```text
BUY_INGREDIENT_STOCK
```

### 6.6. Add recipe action

If price increase is capped:

```text
reduce expensive ingredient by 5–15%
```

### 6.7. Generate reasoning

Example:

```text
Carbonara margin falls below target in month 3.
Worst-case margin reaches 51% by month 6.
Cheese and eggs are the biggest contributors to cost increase.
Olive oil has high upside risk driven by drought and energy costs.
```

### 6.8. Create recommendation endpoint

Endpoint:

```text
POST /api/recommendations/generate
```

## Deliverables

```text
recommendation_engine.py
reasoning_generator.py
/api/recommendations/generate
recommendation_response.json
```

---

# BLOCK 7 — Scenario Engine

## Owner

Backend/product logic person

## Goal

Show adaptive behavior when assumptions change.

## Tasks

### 7.1. Define scenario inputs

```text
target_margin
max_price_increase_percent
supplier_lead_time_weeks
demand_shock_percent
allow_recipe_changes
allow_procurement_stock
risk_tolerance
```

### 7.2. Implement scenario simulation

Endpoint:

```text
POST /api/scenario/simulate
```

### 7.3. Compare old vs new recommendation

Response must show:

```text
old action
new action
what changed
why changed
```

### 7.4. Must-have Sunday scenario

Before:

```text
max_price_increase_percent = 8
supplier_lead_time_weeks = 3
allow_recipe_changes = true
```

After:

```text
max_price_increase_percent = 5
supplier_lead_time_weeks = 8
allow_recipe_changes = false
```

Expected adaptation:

```text
Old:
raise price gradually + recipe optimization

New:
cap price increase + buy ingredient stock + accept temporary margin drop
```

## Deliverables

```text
scenario_engine.py
/api/scenario/simulate
scenario_response.json
```

---

# BLOCK 8 — Frontend and Demo

## Owner

Frontend person

## Goal

Build one-page dashboard for live demo.

## Tasks

### 8.1. Create layout

Sections:

```text
Summary cards
Menu risk table
Ingredient forecast chart
Dish margin chart
Recommendation card
Scenario controls
Reasoning panel
```

### 8.2. Summary cards

Show:

```text
Dishes at Risk
Critical Dishes
Average Margin Drop
Highest Risk Ingredient
Recommended Actions
```

### 8.3. Menu risk table

Columns:

```text
Dish
Current Price
Current Margin
Month 6 Margin
Worst Case Margin
Risk Level
Recommended Action
```

### 8.4. Ingredient forecast chart

Show:

```text
historical price
forecast median
lower confidence band
upper confidence band
```

### 8.5. Dish margin chart

Show:

```text
expected margin
worst-case margin
target margin line
```

### 8.6. Recommendation card

Show:

```text
primary action
new price
price plan
procurement action
recipe action
reasoning
```

### 8.7. Scenario controls

Controls:

```text
Max price increase
Supplier lead time
Recipe changes allowed
Procurement stock allowed
Risk tolerance
Demand shock
```

### 8.8. Demo mode

Frontend must support:

```text
cached API response
mock data fallback
```

## Deliverables

```text
working dashboard
scenario controls
demo mode
```

---

# 13. Backend API Specification

## 13.1. GET /api/dataset/demo

Returns demo restaurant data.

## 13.2. POST /api/forecast/run

Runs forecast for ingredients.

Request:

```json
{
  "ingredients": ["pasta", "tomatoes", "cheese", "olive_oil", "eggs"],
  "horizon_months": 6
}
```

## 13.3. GET /api/forecast/latest

Returns latest normalized ingredient forecasts.

## 13.4. POST /api/menu/analyze

Calculates dish cost and margin forecast.

## 13.5. POST /api/recommendations/generate

Generates actions.

## 13.6. POST /api/scenario/simulate

Simulates changed assumptions.

---

# 14. Suggested Repository Structure

```text
menumargin-ai/
  backend/
    app/
      main.py
      api/
        dataset.py
        forecast.py
        menu.py
        recommendations.py
        scenario.py
      services/
        eurostat_fetcher.py
        price_reconstructor.py
        sybilion_client.py
        forecast_normalizer.py
        dish_cost_engine.py
        margin_engine.py
        recommendation_engine.py
        scenario_engine.py
        reasoning_generator.py
      models/
        schemas.py
      data/
        cache/
        mock/
    requirements.txt

  frontend/
    src/
      components/
        SummaryCards.tsx
        MenuRiskTable.tsx
        IngredientForecastChart.tsx
        DishMarginChart.tsx
        RecommendationCard.tsx
        ScenarioControls.tsx
        ReasoningPanel.tsx
      lib/
        api.ts
      types/
        menu.ts
    package.json

  data/
    config/
      ingredient_sources.csv
      ingredient_keywords.json
    raw/
    processed/
    demo/
      recipes.csv
      menu.csv
      current_prices.csv

  scripts/
    fetch_eurostat_hicp.py
    reconstruct_ingredient_prices.py
    validate_data.py

  docs/
    demo_script.md
    technical_summary.md
    data_methodology.md

  README.md
```

---

# 15. 36-Hour Plan

## Hours 0–2

```text
Lock ingredients
Lock COICOP mapping
Create repo
Create task owners
Create CSV schemas
```

## Hours 2–6

```text
Fetch Eurostat data
Create current price anchors
Reconstruct ingredient_prices.csv
Validate data
Start FastAPI backend
```

## Hours 6–10

```text
Integrate Sybilion API
Run first forecast
Cache response
Create mock fallback
Normalize forecast
```

## Hours 10–16

```text
Build dish cost engine
Build margin engine
Create menu analysis endpoint
Generate margin risk table
```

## Hours 16–22

```text
Build recommendation engine
Add price recommendation
Add procurement actions
Add reasoning
```

## Hours 22–28

```text
Build frontend dashboard
Charts
Tables
Recommendation card
```

## Hours 28–32

```text
Build scenario engine
Add controls
Show old vs new recommendation
```

## Hours 32–36

```text
Polish
Demo mode
Pitch script
Technical summary
Rehearse
```

---

# 16. Priority

## P0

```text
Eurostat data pipeline
current price anchors
ingredient_prices.csv
Sybilion API integration
dish margin engine
recommendation engine
one-page frontend
scenario simulation
cached demo mode
```

## P1

```text
driver importance chart
backtest confidence score
recipe optimization
better UI
technical summary polish
```

## P2

```text
World Bank fallback
ECB conversion
FAO data
EU Agri dashboard parsing
LLM explanation polish
```

---

# 17. Team Assignments

## Person 1 — Data

```text
find Eurostat categories
fetch HICP indices
create current price anchors
reconstruct ingredient_prices.csv
validate 60+ monthly points
```

## Person 2 — Sybilion / Backend API

```text
read Sybilion docs
create API client
run forecast for ingredients
normalize response
cache response
create mock fallback
```

## Person 3 — Backend Logic

```text
dish cost engine
margin engine
recommendation engine
scenario engine
reasoning generator
```

## Person 4 — Frontend

```text
dashboard
charts
tables
scenario controls
recommendation card
demo mode
```

## Person 5 — Pitch / Docs

```text
demo script
technical summary
data methodology
final pitch
slides if needed
```

## Person 6 — Full-stack helper / integration

```text
connect frontend to backend
fix bugs
prepare final demo flow
support data/backend/frontend bottlenecks
```

---

# 18. Data Honesty Statement

Use this in pitch or README:

```text
For the prototype, ingredient cost histories are reconstructed from official European food price indices and current price anchors. This gives us consistent monthly ingredient-level time series while keeping the pipeline reproducible. The system is designed to support real restaurant procurement data when available.
```

---

# 19. Final Demo Script

## Opening

```text
Restaurants do not lose margins all at once. They lose them silently, ingredient by ingredient and dish by dish.
```

## Problem

```text
Ingredient prices move monthly, but menu prices stay fixed for months. By the time the restaurant notices, some dishes are already unprofitable.
```

## Solution

```text
MenuMargin AI forecasts ingredient costs and turns them into dish-level margin protection decisions.
```

## Demo

```text
We use an Italian bistro with three dishes: Margherita Pizza, Pasta Pomodoro, and Carbonara.
```

## Forecast

```text
We forecast key ingredients like pasta, cheese, eggs, olive oil, and tomatoes for the next 6 months.
```

## Margin risk

```text
Carbonara margin falls below target by month 3 and reaches a critical worst-case level by month 6.
```

## Recommendation

```text
The agent recommends gradually increasing the price and buying key ingredients earlier.
```

## Scenario

```text
Now we change assumptions: maximum allowed price increase drops from 8% to 5%, supplier lead time increases to 8 weeks, and recipe changes are disabled.
```

## Adaptation

```text
The agent adapts. It caps the price increase, shifts toward procurement stock, and accepts a temporary margin drop.
```

## Closing

```text
MenuMargin AI does not just forecast ingredient prices. It protects restaurant margins under uncertainty.
```

---

# 20. Final Team Message

```text
We are not building a forecasting dashboard.
We are building a restaurant margin decision agent.

The data pipeline gives us monthly ingredient costs.
Sybilion gives us probabilistic ingredient forecasts.
Our engine converts those forecasts into dish-level margin risk and concrete actions.
The demo proves decision change, visible reasoning, and adaptation under changing assumptions.
```
