# Global Socio-Economic Development: Who Benefits and Why?
______
## Team Prophetable
- Liyan Cheung (lmc9603)  
- Taaha Bin Mohsin (tb3486)

## Why This Matters

Across the world, countries differ not only in wealth, but in health, education, and sustainability. We often assume economic growth naturally improves living conditions — that higher GDP leads to better health care, longer lives, cleaner environments, and lower inequality.

But is that actually true?

If two countries have the same income levels, do people really enjoy the same quality of life? And if countries are achieving rapid economic growth, is it coming at the expense of the environment?

Understanding these relationships matters for:
- policymakers deciding where to allocate funding,
- international development organizations evaluating country progress,
- and ordinary citizens comparing conditions and opportunities across nations.

Our goal is to explore the relationship between economic prosperity and social and environmental outcomes over three decades - and measure how evenly global development has been shared.

---

## Research Questions

This article investigates the following questions:

1. How have GDP per capita and life expectancy evolved across income groups since 1990?
2. Is there a visible correlation between economic growth and social progress (life expectancy, literacy rate), and do countries with similar GDP levels differ in their environmental or social performance?
3. Do higher-income countries have lower poverty rates?
4. Is there a trade-off between economic growth and CO₂ emissions?
5. Which regions show the strongest balance between economic prosperity and sustainability?
6. Have developing countries narrowed the gap with high-income nations in education and health outcomes?
7. Can we identify clusters of countries with similar socio-economic profiles using visualization (e.g., scatterplots or map visualizations)?

Each section of this project presents a question, a visualization, and an interpretation of what the data reveals.

---

## Data Description

### Source
We use the World Bank’s **World Development Indicators**, a comprehensive global dataset constructed from:
- national statistics offices,
- UN agencies,
- and international surveys.

We used the following public mirror of the data:

https://www.kaggle.com/datasets/georgejdinicola/world-bank-indicators/data

### Who collected it?
The World Bank compiles and standardizes the data submissions, harmonizing definitions and ensuring comparability across countries and years.

### Key attributes
We focus on indicators that represent economic, social, and environmental dimensions of development:

- GDP per capita  
- Life expectancy at birth  
- Literacy rate / school enrollment  
- Poverty headcount ratio at \$6.85/day  
- Carbon intensity of GDP (kg CO₂e per 2021 PPP dollar)

### Preprocessing
Our cleaning pipeline included:
- filtering indicators and years (1990–2024),
- handling missing values,
- normalizing or transforming attributes,
- merging with World Bank metadata (region, income group),
- and computing derived attributes when useful.

---

## Where the Article Goes Next

In the following sections, we answer each research question through:
- interactive D3 visualizations,
- statistical comparisons across regions and income groups,
- and interpretive analysis supported by global data.

The goal is to determine whether economic growth alone predicts human well-being and sustainability - or whether countries with similar income levels diverge dramatically in outcomes.
