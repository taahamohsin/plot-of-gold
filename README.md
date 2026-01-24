# Plot of Gold

[![Deploy](https://github.com/taahamohsin/plot-of-gold/actions/workflows/deploy.yml/badge.svg)](https://github.com/taahamohsin/plot-of-gold/actions/workflows/deploy.yml)
[![Observable Framework](https://img.shields.io/badge/Observable-Framework-blue)](https://observablehq.com/framework/)
[![D3.js](https://img.shields.io/badge/D3.js-v7-orange)](https://d3js.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

An interactive data visualization platform exploring the relationship between economic growth, social progress, and environmental sustainability across 227 countries over three decades.

[**View Live Demo →**](https://taahamohsin.github.io/plot-of-gold/)

## Overview

Plot of Gold is an interactive data journalism application that analyzes World Bank development indicators from 1990–2024 to answer a fundamental question: **Does economic growth translate into better lives?**

The platform features 7 interactive visualizations that explore GDP trends, life expectancy, poverty rates, carbon emissions, and regional development patterns—revealing insights that challenge common assumptions about global development.

### Key Findings

- **Health Convergence**: Low-income countries show the steepest life expectancy improvements despite minimal GDP growth
- **Diminishing Returns**: At higher GDP levels, additional wealth produces smaller gains in social outcomes
- **U-Shaped Carbon Curve**: Development initially increases emissions, but high-income countries become more carbon-efficient
- **Policy Over Wealth**: K-Means clustering reveals that environmental sustainability is driven by policy choices, not income level alone

---

## Features

### Interactive Visualizations

| Visualization | Description |
|---------------|-------------|
| **Multi-line Time Series** | GDP and life expectancy trends across income groups with animated transitions |
| **Scatterplots with Regression** | Correlation analysis between GDP and social indicators |
| **Dynamic Boxplots** | Poverty rate distributions by income classification |
| **Choropleth Maps** | Geographic visualization of carbon intensity and sustainability metrics |
| **K-Means Clustering** | Machine learning-powered country segmentation based on 4 economic indicators |

### Technical Highlights

- **Reactive Data Binding**: Observable Framework's reactive runtime enables real-time updates across linked visualizations
- **Responsive Design**: All charts adapt to viewport size with proper aspect ratio preservation
- **Tooltip Interactivity**: Hover states reveal detailed country-level metrics
- **Automated CI/CD**: GitHub Actions pipeline for continuous deployment to GitHub Pages
- **Data Pipeline**: Python preprocessing scripts for cleaning and transforming World Bank datasets

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Visualization** | D3.js v7, Observable Plot |
| **Framework** | Observable Framework |
| **Data Processing** | Python (pandas, numpy) |
| **Styling** | CSS3 with dark mode theme |
| **Deployment** | GitHub Actions, GitHub Pages |
| **Data Source** | World Bank Development Indicators |

---


## Getting Started

### Prerequisites

- Node.js ≥ 18
- Yarn or npm

### Installation

```bash
git clone https://github.com/taahamohsin/plot-of-gold.git

cd plot-of-gold

yarn install

yarn dev
```

Visit [http://localhost:3000](http://localhost:3000) to view the application.

### Build & Deploy

```bash
yarn build

yarn deploy:gh
```

---

## Data Pipeline

The project processes World Bank indicators through a multi-stage pipeline:

1. **Extraction**: Raw CSV data from [Kaggle World Bank Indicators](https://www.kaggle.com/datasets/georgejdinicola/world-bank-indicators/data)
2. **Transformation**: Python scripts filter years (1990–2024), handle missing values, normalize attributes
3. **Enrichment**: Merge with World Bank metadata (region, income group classifications)
4. **Aggregation**: Compute derived metrics (carbon intensity, regional averages)

---

## Visualizations Deep Dive

### 1. GDP & Life Expectancy Trends
Multi-line chart showing divergent economic trajectories alongside convergent health outcomes across income groups.

### 2. Social Progress Correlation
Interactive scatterplot with regression line demonstrating diminishing returns of GDP on life expectancy and literacy.

### 3. Poverty Distribution Analysis
Boxplots revealing institutional factors beyond GDP that determine poverty outcomes.

### 4. Carbon-GDP Trade-off
Analysis of the environmental Kuznets curve showing the U-shaped relationship between development and emissions.

### 5. Regional Sustainability Index
Comparative choropleth highlighting which regions achieve the best balance between prosperity and sustainability.

### 6. Development Gap Convergence
Time series showing how developing countries are catching up in education and health metrics.

### 7. Country Clustering
K-Means segmentation (k=4) identifying distinct development profiles based on GDP, renewable energy, GHG emissions, and inflation.

---

## Commands Reference

| Command | Description |
|---------|-------------|
| `yarn install` | Install dependencies |
| `yarn dev` | Start local development server |
| `yarn build` | Build production bundle to `./dist` |
| `yarn clean` | Clear data loader cache |
| `yarn deploy:gh` | Deploy to GitHub Pages |

---

## License

This project is licensed under the MIT License.

---

## Acknowledgments

- Data provided by the [World Bank Open Data](https://data.worldbank.org/)
- Built with [Observable Framework](https://observablehq.com/framework/)
- Visualizations powered by [D3.js](https://d3js.org/)
