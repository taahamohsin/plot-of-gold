---
draft: true
---

# Final Project - Milestone #3: First Draft

## Brief introduction to the project

Economic growth and goals like improving social well-being and protecting the environment are often at odds with one another for countries as they develop. Our project investigates this tension by examining how key World Bank development indicators relate to one another across countries. Using metrics such as GDP per capita, life expectancy, educational attainment, inequality, and carbon emissions, we aim to explore whether rising national income reliably translates into better social outcomes, or whether economic gains sometimes come with environmental or social costs.

We explore this in the form of seven domain questions:
1. How have GDP per capita and life expectancy evolved across income groups since 1990?
2. Is there a visible correlation between economic growth and social progress (life expectancy, literacy rate), and do countries with similar GDP levels differ in their environmental or social performance?
3. Do higher-income countries have lower poverty rates?
4. Is there a trade-off between economic growth and CO₂ emissions?
5. Which regions show the strongest balance between economic prosperity and sustainability?
6. Have developing countries narrowed the gap with high-income nations in education and health outcomes?
7. Can we identify clusters of countries with similar socio-economic profiles using visualization (e.g., scatterplots or map visualizations)?

```js
const gdpData = await FileAttachment("gdp_lifeexpectancy.csv").csv();
```

```js echo
{
  const margin = { top: 30, right: 160, bottom: 40, left: 60 };
  const width = 650 - margin.left - margin.right;
  const height = 300 - margin.top - margin.bottom;

  const svg = d3.create("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom);

  const g = svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

  const filtered = gdpData.filter(d => +d.year >= 1990);

  const nested = d3.groups(filtered, d => d.income_group, d => d.year)
    .map(([income_group, yearGroups]) => ({
      income_group,
      values: yearGroups
        .map(([year, rows]) => ({
          year: +year,
          gdp_pc: d3.mean(rows, r => +r["GDP per capita (current US$)"])
        }))
        .sort((a, b) => a.year - b.year)
    }));

  const x = d3.scaleLinear()
      .domain(d3.extent(filtered, d => +d.year))
      .range([0, width]);

  const y = d3.scaleLinear()
      .domain([0, d3.max(nested, g => d3.max(g.values, d => d.gdp_pc))])
      .nice()
      .range([height, 0]);

  const color = d3.scaleOrdinal()
      .domain(nested.map(d => d.income_group))
      .range(d3.schemeTableau10);

  g.append("g")
      .attr("transform", `translate(0,${height})`)
      .call(d3.axisBottom(x).tickFormat(d3.format("d")));

  g.append("g")
      .call(d3.axisLeft(y));

  g.append("text")
      .attr("x", width / 2)
      .attr("y", height + 35)
      .attr("text-anchor", "middle")
      .text("Year");

  g.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", -45)
      .attr("x", -(height / 2))
      .attr("text-anchor", "middle")
      .text("GDP per Capita (USD, mean)");

  const line = d3.line()
      .x(d => x(d.year))
      .y(d => y(d.gdp_pc));

  g.selectAll(".line-group")
    .data(nested)
    .enter()
    .append("path")
      .attr("fill", "none")
      .attr("stroke", d => color(d.income_group))
      .attr("stroke-width", 2)
      .attr("d", d => line(d.values));

  const legend = g.append("g")
      .attr("transform", `translate(${width + 15}, 0)`);

  nested.forEach((group, i) => {
    const yOffset = i * 20;

    legend.append("rect")
      .attr("x", 0)
      .attr("y", yOffset)
      .attr("width", 12)
      .attr("height", 12)
      .attr("fill", color(group.income_group));

    legend.append("text")
      .attr("x", 20)
      .attr("y", yOffset + 10)
      .text(group.income_group)
      .style("font-size", "12px");
  });

  display(svg.node());
}
```

```js echo
{
  const margin = { top: 30, right: 160, bottom: 40, left: 60 };
  const width = 650 - margin.left - margin.right;
  const height = 300 - margin.top - margin.bottom;

  const svg = d3.create("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom);

  const g = svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

  const filtered = gdpData.filter(d => +d.year >= 1990);

  const grouped = d3.groups(filtered, d => d.income_group, d => d.year);

  const nested = [];
  const allLife = [];

  for (const [income_group, yearGroups] of grouped) {
    const values = [];

    for (const [year, rows] of yearGroups) {
      const vals = rows
        .map(r => {
          const raw = r["Life expectancy at birth, total (years)"];
          if (raw === "" || raw == null) return NaN;
          const num = +raw;
          return Number.isFinite(num) ? num : NaN;
        })
        .filter(Number.isFinite);

      if (vals.length === 0) continue;

      const life = d3.mean(vals);
      values.push({ year: +year, life_exp: life });
      allLife.push(life);
    }

    values.sort((a, b) => a.year - b.year);

    if (values.length > 0) {
      nested.push({ income_group, values });
    }
  }

  const x = d3.scaleLinear()
      .domain(d3.extent(filtered, d => +d.year))
      .range([0, width]);

  const y = d3.scaleLinear()
      .domain(d3.extent(allLife))
      .nice()
      .range([height, 0]);

  const color = d3.scaleOrdinal()
      .domain(nested.map(d => d.income_group))
      .range(d3.schemeTableau10);

  g.append("g")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x).tickFormat(d3.format("d")));

  g.append("g")
    .call(d3.axisLeft(y));

  g.append("text")
      .attr("x", width / 2)
      .attr("y", height + 35)
      .attr("text-anchor", "middle")
      .text("Year");

  g.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", -45)
      .attr("x", -(height / 2))
      .attr("text-anchor", "middle")
      .text("Life Expectancy (years, mean)");

  const line = d3.line()
      .x(d => x(d.year))
      .y(d => y(d.life_exp));

  g.selectAll(".line-group")
    .data(nested)
    .enter()
    .append("path")
      .attr("fill", "none")
      .attr("stroke", d => color(d.income_group))
      .attr("stroke-width", 2)
      .attr("d", d => line(d.values));

  const legend = g.append("g")
      .attr("transform", `translate(${width + 15}, 0)`);

  nested.forEach((group, i) => {
    const yOffset = i * 20;

    legend.append("rect")
      .attr("x", 0)
      .attr("y", yOffset)
      .attr("width", 12)
      .attr("height", 12)
      .attr("fill", color(group.income_group));

    legend.append("text")
      .attr("x", 20)
      .attr("y", yOffset + 10)
      .text(group.income_group)
      .style("font-size", "12px");
  });

  return svg.node();
}

```

## Q1: How have GDP per capita and life expectancy evolved across income groups since 1990?
-------
## Describe what the visualization shows
The line chart plots the mean GDP per capita for each World Bank income group from 1990 to 2023. Each colored line represents a different income group, allowing direct comparison of long-term economic trends. The High income group sits far above all others and shows a steady upward trajectory, especially after the early 2000s. Upper middle income countries show moderate but consistent growth over the entire period. Lower middle income and Low income countries remain clustered near the bottom of the chart, with much lower GDP per capita and slower growth rates. The “Not classified” category fluctuates irregularly due to sparse or inconsistent country classifications. Overall, the visualization clearly illustrates the persistent income gap between groups and the widening distance between high-income economies and the rest.

## Answer the question based on the visualization
Based on the GDP per capita trends alone, economic outcomes have diverged significantly across income groups since 1990. High-income countries have experienced the strongest and most sustained growth, with GDP per capita rising from roughly $13,000 in 1990 to nearly $50,000 by 2023. Upper-middle-income countries also show upward progress, though at a much lower absolute level. In contrast, lower-middle-income and low-income groups exhibit only modest gains and remain far behind, indicating that global income disparities have persisted and in some cases widened.

Given the typical relationship between income and health outcomes—and as supported by global development literature—these economic patterns imply that life expectancy has likely increased more rapidly in high-income and upper-middle-income groups than in lower-income groups. The widening GDP per capita gap suggests that improvements in health, healthcare access, and longevity have not been evenly distributed. Thus, both GDP per capita and life expectancy have improved overall since 1990, but the pace and magnitude of improvement differ sharply by income group, with high-income countries seeing the largest gains.

```js echo
q2data = await FileAttachment("q2_gdp_life_literacy@1.csv").csv();
```

```js echo
{
  const margin = { top: 30, right: 200, bottom: 50, left: 65 };
  const width = 700 - margin.left - margin.right;
  const height = 430 - margin.top - margin.bottom;

  const svg = d3.create("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom);

  const g = svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

  const color = d3.scaleOrdinal()
    .domain(["<60%", "60-80%", "80-90%", "90-100%"])
    .range(["#d73027", "#fc8d59", "#91bfdb", "#1a9850"]);

  const xVals = q2data
    .map(d => +d["GDP per capita (current US$)"])
    .filter(Number.isFinite);

  const yVals = q2data
    .map(d => +d["Life expectancy at birth, total (years)"])
    .filter(Number.isFinite);

  const x = d3.scaleLog()
    .domain(d3.extent(xVals))
    .nice()
    .range([0, width]);

  const y = d3.scaleLinear()
    .domain(d3.extent(yVals))
    .nice()
    .range([height, 0]);

  g.append("g")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x).ticks(10, "~s"));

  g.append("g")
    .call(d3.axisLeft(y));

  g.append("text")
    .attr("x", width / 2)
    .attr("y", height + 40)
    .attr("text-anchor", "middle")
    .text("GDP per Capita (USD, log scale)");

  g.append("text")
    .attr("transform", "rotate(-90)")
    .attr("x", -(height / 2))
    .attr("y", -50)
    .attr("text-anchor", "middle")
    .text("Life Expectancy (years)");

  d3.select("body").selectAll(".tooltip").remove();

  const tooltip = d3.select("body")
    .append("div")
      .attr("class", "tooltip")
      .style("position", "absolute")
      .style("background", "white")
      .style("padding", "8px 10px")
      .style("border", "1px solid #ccc")
      .style("border-radius", "4px")
      .style("pointer-events", "none")
      .style("opacity", 0)
      .style("font-size", "12px");

  g.selectAll("circle")
    .data(q2data)
    .enter()
    .append("circle")
      .attr("cx", d => x(+d["GDP per capita (current US$)"]))
      .attr("cy", d => y(+d["Life expectancy at birth, total (years)"]))
      .attr("r", Math.sqrt(80 / Math.PI))
      .attr("fill", d => color(d.literacy_bucket))
      .attr("opacity", 0.75)
      .on("mouseover", (event, d) => {
        tooltip.style("opacity", 1)
          .html(`
            <b>${d.country_name}</b><br>
            Income Group: ${d.income_group}
          `);
      })
      .on("mousemove", (event) => {
        tooltip
          .style("left", (event.pageX + 15) + "px")
          .style("top", (event.pageY - 28) + "px");
      })
      .on("mouseleave", () => {
        tooltip.style("opacity", 0);
      });

  const legend = g.append("g")
    .attr("transform", `translate(${width + 10}, 10)`);

  legend.append("text")
        .attr("y", -15)
        .attr("font-size", "14px")
        .attr("font-weight", "bold")
        .text("Literacy rate");

  const buckets = color.domain();

  buckets.forEach((bucket, i) => {
    const yOffset = i * 20;

    legend.append("rect")
      .attr("x", 0)
      .attr("y", yOffset)
      .attr("width", 12)
      .attr("height", 12)
      .attr("fill", color(bucket));

    legend.append("text")
      .attr("x", 20)
      .attr("y", yOffset + 10)
      .text(bucket)
      .style("font-size", "12px");
  });

  return svg.node();
}

```

```js echo
{
  const facetWidth = 600;
  const facetHeight = 260;
  const margin = { top: 50, right: 40, bottom: 60, left: 80 };

  const tiers = ["Low GDP", "Lower-Mid GDP", "Upper-Mid GDP", "High GDP"];

  const color = d3.scaleOrdinal()
    .domain(["High income", "Low income", "Lower middle income", "Not classified", "Upper middle income"])
    .range(["#4c72b0", "#dd8452", "#c44e52", "#55a3b1", "#81c16b"]);

  const size = d3.scaleSqrt()
    .domain([0, 100])
    .range([4, 20]);

  const wrapper = d3.create("div")
    .style("position", "relative")
    .style("width", (facetWidth + margin.left + margin.right + 260) + "px");

  const gdpValues = q2data.map(d => +d["GDP per capita (current US$)"]).filter(d => d > 0);
  const xMin = d3.quantile(gdpValues, 0.02);
  const xMax = d3.quantile(gdpValues, 0.98);

  const xPadding = 20;
  const innerWidth = facetWidth - xPadding * 2;

  const x = d3.scaleLog()
    .domain([xMin, xMax])
    .range([xPadding, facetWidth - xPadding])
    .clamp(true);

  const y = d3.scaleLinear()
    .domain([20, 100])
    .range([facetHeight, 0])
    .nice();

  const xTicks = [200, 500, 1000, 2000, 5000, 10000, 20000];

  tiers.forEach(tier => {
    const svg = wrapper.append("svg")
      .attr("width", facetWidth + margin.left + margin.right)
      .attr("height", facetHeight + margin.top + margin.bottom)
      .style("display", "block");

    const g = svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    const data = q2data.filter(d => d.gdp_tier === tier);

    g.append("g")
      .attr("transform", `translate(0,${facetHeight})`)
      .call(
        d3.axisBottom(x)
          .tickValues(xTicks)
          .tickFormat(d3.format("~s"))
          .tickSize(-facetHeight)
      );

    g.append("g")
      .call(
        d3.axisLeft(y)
          .tickSize(-innerWidth)
      );

    g.selectAll("circle")
      .data(data)
      .join("circle")
      .attr("cx", d => x(+d["GDP per capita (current US$)"]))
      .attr("cy", d => y(+d["Literacy rate, adult total (% of people ages 15 and above)"]))
      .attr("r", d => size(+d["Life expectancy at birth, total (years)"]))
      .attr("opacity", 0.75)
      .attr("fill", d => color(d.income_group));

    svg.append("text")
      .attr("x", margin.left)
      .attr("y", 35)
      .attr("font-size", "26px")
      .attr("font-weight", "700")
      .text(tier);

    svg.append("text")
      .attr("x", margin.left + facetWidth / 2)
      .attr("y", facetHeight + margin.top + 45)
      .attr("text-anchor", "middle")
      .attr("font-size", "14px")
      .text("GDP per Capita (USD, log)");

    svg.append("text")
      .attr("transform", `translate(${margin.left - 50},${margin.top + facetHeight / 2}) rotate(-90)`)
      .attr("text-anchor", "middle")
      .attr("font-size", "14px")
      .text("Literacy Rate (%)");
  });

  const legend = wrapper.append("svg")
    .attr("width", 260)
    .attr("height", 450)
    .style("position", "absolute")
    .style("right", "0px")
    .style("top", "80px");

  legend.append("text")
    .attr("x", 10)
    .attr("y", 20)
    .attr("font-size", "22px")
    .attr("font-weight", "700")
    .text("Income Group");

  ["High income", "Low income", "Lower middle income", "Not classified", "Upper middle income"]
    .forEach((group, i) => {
      legend.append("circle")
        .attr("cx", 15)
        .attr("cy", 55 + i * 30)
        .attr("r", 9)
        .attr("fill", color(group));
      legend.append("text")
        .attr("x", 35)
        .attr("y", 60 + i * 30)
        .attr("font-size", "15px")
        .text(group);
    });

  legend.append("text")
    .attr("x", 10)
    .attr("y", 220)
    .attr("font-size", "22px")
    .attr("font-weight", "700")
    .text("Life Expectancy (years)");

  [0, 20, 40, 60, 80].forEach((v, i) => {
    legend.append("circle")
      .attr("cx", 35)
      .attr("cy", 260 + i * 35)
      .attr("r", size(v))
      .attr("fill", "gray")
      .attr("opacity", 0.4);
    legend.append("text")
      .attr("x", 80)
      .attr("y", 265 + i * 35)
      .attr("font-size", "15px")
      .text(v);
  });

  return wrapper.node();
}

```

## Q2: Is there a visible correlation between economic growth and social progress (e.g., life expectancy, literacy rate), and do countries with similar GDP levels differ in their social performance?
------
## Describe the visualization
The first scatterplot (GDP vs. life expectancy) shows a clear upward trend: as GDP per capita increases, countries generally have higher life expectancy. Points also become more dominated by high-literacy categories (80-90% and 90-100%) at higher GDP levels, while low-income countries cluster at the lower end of both axes. This indicates that richer countries tend to have better health and education outcomes. The faceted charts break the same dataset into four economic tiers (“Low GDP,” “Lower-Mid GDP,” “Upper-Mid GDP,” and “High GDP”), revealing how social indicators vary within each income bracket.
The Low-GDP panel shows large variation in both literacy and life expectancy, and most countries fall into low or lower-middle income groups. The Lower-Mid GDP group shows tighter clustering with moderate literacy and life expectancy. The Upper-Mid GDP panel is dominated by high literacy and high life expectancy. The High-GDP panel is extremely dense near the very top of both scales, with nearly all countries showing >90% literacy and 80-85+ years of life expectancy. Across all panels, circle size (life expectancy) and color (income group) consistently shift upward as GDP increases, visually reinforcing the overall trend.

## Answer the question based on the visualization
There is a strong and visible correlation between economic growth and social progress. Both the combined scatterplot and the four faceted charts show that countries with higher GDP per capita almost always exhibit higher literacy rates and longer life expectancy. The relationship is monotonic and persistent across all tiers: no high-GDP country has low literacy or low life expectancy, while many low-GDP countries do.
Countries with similar GDP levels do differ in their social outcomes, but less so at higher income levels. In the Low-GDP tier, social progress varies dramatically. Some countries achieve literacy rates above 80% and relatively high life expectancy despite low GDP, while others with the same GDP level lag significantly behind. This suggests that policy, governance, or regional factors play a major role when resources are limited. In the Lower-Mid GDP tier, variation narrows but is still notable. Countries in this range can differ by 20+ percentage points in literacy despite having similar GDP per capita. In the Upper-Mid GDP tier, social outcomes become more uniform.
Most countries reach high literacy rates and life expectancy converges around the upper 70s to low 80s. In the High-GDP tier, differences are almost completely non-existent. Nearly all countries have >90% literacy and long life expectancy, indicating that once GDP crosses a high threshold, social indicators flatten out.

```js echo
povertyData = await FileAttachment("q3_poverty_filled.csv").csv();
```

```js echo
{
  const margin = { top: 40, right: 20, bottom: 110, left: 70 };
  const width = 520 - margin.left - margin.right;
  const height = 420 - margin.top - margin.bottom;

  const svg = d3.create("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom + 20);

  const g = svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

  const valid = povertyData.filter(
    d => d.poverty_rate_6_85 != null && d.poverty_rate_6_85 !== "" && Number.isFinite(+d.poverty_rate_6_85)
  );

  const order = [
    "Low income",
    "Lower middle income",
    "Upper middle income",
    "High income",
    "Not classified"
  ];

  const grouped = d3.groups(valid, d => d.income_group)
    .map(([income_group, rows]) => ({
      income_group,
      median: d3.median(rows, r => +r.poverty_rate_6_85)
    }))
    .filter(d => order.includes(d.income_group))
    .sort((a, b) => order.indexOf(a.income_group) - order.indexOf(b.income_group));

  const x = d3.scaleBand()
      .domain(grouped.map(d => d.income_group))
      .range([0, width])
      .padding(0.2);

  const y = d3.scaleLinear()
      .domain([0, d3.max(grouped, d => d.median)])
      .nice()
      .range([height, 0]);

g.append("g")
  .attr("transform", `translate(0,${height})`)
  .call(d3.axisBottom(x))
  .selectAll("text")
    .attr("transform", "rotate(90)")
    .style("text-anchor", "start")
    .attr("dx", "0.8em")
    .attr("dy", "-0.2em");
  
  g.append("g")
    .call(d3.axisLeft(y));

  g.append("text")
    .attr("x", width / 2)
    .attr("y", height + 125)
    .attr("text-anchor", "middle")
    .text("Income Group");

  g.append("text")
    .attr("transform", "rotate(-90)")
    .attr("x", -(height / 2))
    .attr("y", -55)
    .attr("text-anchor", "middle")
    .text("Median Poverty Rate (%)");

  g.append("text")
    .attr("x", width / 2)
    .attr("y", -10)
    .attr("text-anchor", "middle")
    .style("font-size", "15px")
    .style("font-weight", "bold")
    .text("Do Higher-Income Countries Have Lower Poverty Rates?");

  g.selectAll("rect")
    .data(grouped)
    .enter()
    .append("rect")
      .attr("x", d => x(d.income_group))
      .attr("y", d => y(d.median))
      .attr("width", x.bandwidth())
      .attr("height", d => height - y(d.median))
      .attr("fill", "#4682b4");

  return svg.node();
}

```

```js echo
{
  const margin = { top: 30, right: 20, bottom: 30, left: 70 };
  const width = 520 - margin.left - margin.right;
  const height = 260 - margin.top - margin.bottom;

  const svg = d3.create("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom + 100);

  const g = svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

  const valid = povertyData.filter(
    d => d.poverty_rate_6_85 != null &&
         d.poverty_rate_6_85 !== "" &&
         Number.isFinite(+d.poverty_rate_6_85)
  );

  const order = [
    "Low income",
    "Lower middle income",
    "Upper middle income",
    "High income",
    "Not classified"
  ];

  const grouped = d3.groups(valid, d => d.income_group)
    .map(([income_group, rows]) => {
      const values = rows.map(r => +r.poverty_rate_6_85).sort(d3.ascending);

      return {
        income_group,
        values,
        min: d3.min(values),
        q1: d3.quantile(values, 0.25),
        median: d3.quantile(values, 0.5),
        q3: d3.quantile(values, 0.75),
        max: d3.max(values)
      };
    })
    .filter(d => order.includes(d.income_group))
    .sort((a, b) => order.indexOf(a.income_group) - order.indexOf(b.income_group));

  const x = d3.scaleBand()
      .domain(grouped.map(d => d.income_group))
      .range([0, width])
      .padding(0.4);

  const y = d3.scaleLinear()
      .domain([
        d3.min(grouped, d => d.min),
        d3.max(grouped, d => d.max)
      ])
      .nice()
      .range([height, 0]);

  const xAxis = g.append("g")
      .attr("transform", `translate(0,${height})`)
      .call(d3.axisBottom(x));

  xAxis.selectAll("text")
      .attr("transform", "rotate(90)")
      .style("text-anchor", "start")
      .attr("dx", "0.6em")
      .attr("dy", "0.1em");

  g.append("g").call(d3.axisLeft(y));

  g.append("text")
    .attr("x", width / 2)
    .attr("y", height + 125)
    .attr("text-anchor", "middle")
    .text("Income Group");

  g.append("text")
    .attr("transform", "rotate(-90)")
    .attr("x", -(height / 2))
    .attr("y", -55)
    .attr("text-anchor", "middle")
    .text("Poverty Rate (%)");

  const boxColor = "#4682b4";

  g.selectAll(".whisker")
    .data(grouped)
    .enter()
    .append("line")
      .attr("class", "whisker")
      .attr("x1", d => x(d.income_group) + x.bandwidth() / 2)
      .attr("x2", d => x(d.income_group) + x.bandwidth() / 2)
      .attr("y1", d => y(d.min))
      .attr("y2", d => y(d.max))
      .attr("stroke", "black");

  g.selectAll(".box")
    .data(grouped)
    .enter()
    .append("rect")
      .attr("class", "box")
      .attr("x", d => x(d.income_group))
      .attr("width", x.bandwidth())
      .attr("y", d => y(d.q3))
      .attr("height", d => y(d.q1) - y(d.q3))
      .attr("fill", boxColor)
      .attr("opacity", 0.7);

  g.selectAll(".median")
    .data(grouped)
    .enter()
    .append("line")
      .attr("class", "median")
      .attr("x1", d => x(d.income_group))
      .attr("x2", d => x(d.income_group) + x.bandwidth())
      .attr("y1", d => y(d.median))
      .attr("y2", d => y(d.median))
      .attr("stroke", "black")
      .attr("stroke-width", 2);

  g.append("text")
      .attr("x", width / 2)
      .attr("y", -10)
      .attr("text-anchor", "middle")
      .style("font-size", "16px")
      .style("font-weight", "bold")
      .text("Poverty Rate Distribution by Income Group");

  return svg.node();
}

```

# Question 3: Do higher-income countries have lower poverty rates?
--------
# Describe what the visualizations show
The first visualization, a boxplot of poverty rates across income groups, shows the full distribution of poverty outcomes within each category. Low-income countries exhibit extremely high poverty rates that cluster tightly around 85–95%, indicating both high levels and low variability. Lower-middle-income countries have much wider dispersion, with poverty rates ranging from about 40% to over 90%, and a median in the mid-70s. Upper-middle-income countries show a dramatic shift downward, with most poverty rates falling between 10% and 35%. High-income countries display the lowest rates overall — medians near zero and only very small variation — and the “Not classified” group shows relatively high poverty concentrated around the mid-60s.

The second visualization, a bar chart, summarizes the same data by showing the median poverty rate for each income group. Low-income countries have the highest median poverty rate (around 90%), followed by lower-middle-income countries (mid-70s). Upper-middle-income countries show a sharp decline to about 20%, and high-income countries display near-zero median poverty. The “Not classified” group again aligns more closely with lower-middle-income countries.

# Answer the question based on the visualization

Yes. Both visualizations provide strong and consistent evidence that higher-income countries have substantially lower poverty rates. As income level increases, the median poverty rate drops sharply, and the overall distribution of poverty narrows. Low- and lower-middle-income countries face persistently high poverty levels with wide variation, while upper-middle-income countries show substantially lower poverty, and high-income countries maintain near-zero poverty with minimal spread. Together, the boxplot and median bar chart clearly demonstrate a strong negative relationship between national income level and poverty: higher-income countries consistently experience far lower poverty rates.

```js echo
envData = await FileAttachment("q4_env_merged.csv").csv();
```

```js echo
{
  const margin = { top: 50, right: 20, bottom: 60, left: 80 };
  const width = 900 - margin.left - margin.right;
  const height = 500 - margin.top - margin.bottom;

  const svg = d3.create("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom);

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);


  const filtered = envData.filter(d => 
    +d["Carbon intensity of GDP (kg CO2e per 2021 PPP $ of GDP)"] > 0 &&
    +d["GDP per capita (current US$)"] > 0
  );


  const x = d3.scaleLog()
    .domain(d3.extent(filtered, d => +d["GDP per capita (current US$)"]))
    .nice()
    .range([0, width]);

  const y = d3.scaleLog()
    .domain(d3.extent(filtered, d => 
      +d["Carbon intensity of GDP (kg CO2e per 2021 PPP $ of GDP)"]
    ))
    .nice()
    .range([height, 0]);

  const color = d3.scaleOrdinal()
    .domain([...new Set(filtered.map(d => d.income_group))])
    .range(d3.schemeTableau10);

  g.append("g")
    .attr("transform", `translate(0,${height})`)
    .call(
      d3.axisBottom(x)
        .ticks(10, "~s")
    );

  g.append("g")
    .call(
      d3.axisLeft(y)
        .ticks(10, "~s")
    );

  g.append("text")
    .attr("x", width / 2)
    .attr("y", height + 45)
    .attr("text-anchor", "middle")
    .text("GDP per capita (current US$, log scale)");

  g.append("text")
    .attr("transform", "rotate(-90)")
    .attr("x", -(height / 2))
    .attr("y", -55)
    .attr("text-anchor", "middle")
    .text("Carbon intensity of GDP (log scale)");

  d3.select("body").selectAll(".env-tooltip").remove();

  const tooltip = d3.select("body")
    .append("div")
    .attr("class", "env-tooltip")
    .style("position", "absolute")
    .style("background", "white")
    .style("padding", "8px 10px")
    .style("border", "1px solid #ccc")
    .style("border-radius", "4px")
    .style("pointer-events", "none")
    .style("opacity", 0)
    .style("font-size", "12px");

  g.selectAll("circle")
    .data(filtered)
    .enter()
    .append("circle")
      .attr("cx", d => x(+d["GDP per capita (current US$)"]))
      .attr("cy", d => y(+d["Carbon intensity of GDP (kg CO2e per 2021 PPP $ of GDP)"]))
      .attr("r", 6)
      .attr("fill", d => color(d.income_group))
      .attr("opacity", 0.7)
      .on("mouseover", (event, d) => {
        tooltip.style("opacity", 1).html(`
          <b>${d.country_name}</b><br>
          Income group: ${d.income_group}
        `);
      })
      .on("mousemove", event => {
        tooltip
          .style("left", event.pageX + 15 + "px")
          .style("top", event.pageY - 28 + "px");
      })
      .on("mouseleave", () => tooltip.style("opacity", 0));

  g.append("text")
    .attr("x", width / 2)
    .attr("y", -20)
    .attr("text-anchor", "middle")
    .style("font-size", "18px")
    .style("font-weight", "bold")
    .text("Is There a Trade-Off Between Economic Growth and Carbon Efficiency?");

  return svg.node();
}

```

```js echo
{
  const margin = { top: 50, right: 20, bottom: 80, left: 90 };
  const width = 600 - margin.left - margin.right;
  const height = 400 - margin.top - margin.bottom;

  const svg = d3.create("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom + 60);

  const g = svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

  const filtered = envData.filter(d =>
    +d["Carbon intensity of GDP (kg CO2e per 2021 PPP $ of GDP)"] > 0
  );

  const order = [
    "Low income",
    "Lower middle income",
    "Upper middle income",
    "High income"
  ];

  const grouped = d3.groups(filtered, d => d.income_group)
    .map(([income_group, rows]) => {
      if (!order.includes(income_group)) return null;

      const values = rows
        .map(r => +r["Carbon intensity of GDP (kg CO2e per 2021 PPP $ of GDP)"])
        .filter(v => v > 0)
        .sort(d3.ascending);

      return {
        income_group,
        values,
        min: d3.min(values),
        q1: d3.quantile(values, 0.25),
        median: d3.quantile(values, 0.5),
        q3: d3.quantile(values, 0.75),
        max: d3.max(values)
      };
    })
    .filter(d => d !== null)
    .sort((a, b) => order.indexOf(a.income_group) - order.indexOf(b.income_group));

  const x = d3.scaleBand()
      .domain(order)
      .range([0, width])
      .padding(0.4);

  const y = d3.scaleLog()
      .domain([
        d3.min(grouped, d => d.min),
        d3.max(grouped, d => d.max)
      ])
      .nice()
      .range([height, 0]);

  const color = d3.scaleOrdinal()
      .domain(order)
      .range(d3.schemeTableau10);

  const xAxis = g.append("g")
      .attr("transform", `translate(0,${height})`)
      .call(d3.axisBottom(x));

  xAxis.selectAll("text")
      .attr("transform", "rotate(90)")
      .style("text-anchor", "start")
      .attr("dx", "0.6em")
      .attr("dy", "0.2em");

  g.append("g")
      .call(d3.axisLeft(y).ticks(8, "~s"));

  g.append("text")
      .attr("x", width / 2)
      .attr("y", height + 130)
      .attr("text-anchor", "middle")
      .text("Income Group");

  g.append("text")
      .attr("transform", "rotate(-90)")
      .attr("x", -(height / 2))
      .attr("y", -60)
      .attr("text-anchor", "middle")
      .text("Carbon Intensity (kg CO₂ per PPP$ GDP, log scale)");

  g.selectAll(".whisker")
    .data(grouped)
    .enter()
    .append("line")
      .attr("class", "whisker")
      .attr("x1", d => x(d.income_group) + x.bandwidth() / 2)
      .attr("x2", d => x(d.income_group) + x.bandwidth() / 2)
      .attr("y1", d => y(d.min))
      .attr("y2", d => y(d.max))
      .attr("stroke", "black");

  g.selectAll(".box")
    .data(grouped)
    .enter()
    .append("rect")
      .attr("class", "box")
      .attr("x", d => x(d.income_group))
      .attr("width", x.bandwidth())
      .attr("y", d => y(d.q3))
      .attr("height", d => y(d.q1) - y(d.q3))
      .attr("fill", d => color(d.income_group))
      .attr("opacity", 0.6);

  g.selectAll(".median")
    .data(grouped)
    .enter()
    .append("line")
      .attr("class", "median")
      .attr("x1", d => x(d.income_group))
      .attr("x2", d => x(d.income_group) + x.bandwidth())
      .attr("y1", d => y(d.median))
      .attr("y2", d => y(d.median))
      .attr("stroke", "black")
      .attr("stroke-width", 2);

  g.append("text")
      .attr("x", width / 2)
      .attr("y", -20)
      .attr("text-anchor", "middle")
      .style("font-size", "18px")
      .style("font-weight", "bold")
      .text("Carbon Intensity Distribution by Income Group");

  return svg.node();
}

```

# Question 4: Is There a Trade-Off Between Economic Growth and Carbon Efficiency?
-------
## Describe what the visualization shows
The scatterplot compares GDP per capita with the carbon intensity of GDP on log–log scales, using color to differentiate income groups. Across the full income spectrum, carbon intensity remains within a fairly tight band, and there is no upward trend suggesting that wealthier countries emit more carbon per unit of economic output. Low-income countries cluster at the lower end of intensity, while lower-middle- and upper-middle-income countries display higher and more dispersed values. High-income countries, despite much higher GDP per capita, generally occupy the lower end of the carbon-intensity range and show more consistency than middle-income countries. The accompanying boxplot reinforces these patterns: carbon intensity tends to be lowest in low-income countries, rises among lower-middle- and upper-middle-income economies, and then declines again for high-income countries. This creates a U-shaped distribution in which the middle-income tiers exhibit the highest carbon intensity, whereas the richest countries show more efficient output relative to their emissions.

## Answer the question based on the visualization
No. The visualizations do not show a trade-off between economic growth and carbon efficiency. A trade-off would imply that as countries grow richer (higher GDP per capita), they become less carbon-efficient—i.e., carbon intensity should rise with GDP. The evidence here shows the opposite. High-income countries have lower carbon intensity than both lower-middle and upper-middle-income countries. The scatterplot shows no positive relationship between GDP per capita and carbon intensity across the full range. Carbon intensity peaks in the middle, not at the top of the income distribution. Taken together, the charts indicate that middle-income economies tend to be the least carbon-efficient, likely due to energy mix and industrial structure. High-income economies tend to become more efficient, not less, as they grow—possibly due to cleaner energy, more efficient technologies, and economic shifts toward services

```js echo
prospAndSust = FileAttachment("prosperity_sustainability.csv").csv(); 
```

Domain Question #5 

```js echo
// GDP per capita vs total greenhouse gas 
vl.markCircle() 
  .data(prospAndSust)
  .encode(
    vl.x().fieldQ("gdp per capita (current us$)"), 
    vl.y().fieldQ("total greenhouse gas emissions excluding lulucf per capita (t co2e/capita)"),
    vl.tooltip().fieldN("country")
  )
  .render(); 
```

```js echo
// GDP vs. Total Greenhouse Gas Emissions
{
  const dims = {
    width: 810,  
    height: 620,  
    margin_top: 60,
    margin_right: 30,
    margin_bottom: 60,
    margin_left: 80
  };

  const innerWidth = dims.width - dims.margin_left - dims.margin_right;
  const innerHeight = dims.height - dims.margin_top - dims.margin_bottom;

  const svg = d3.create('svg')
    .attr('width', dims.width)
    .attr('height', dims.height);

  const chart = svg.append('g')
    .attr('transform', `translate(${dims.margin_left}, ${dims.margin_top})`);
    
  const gdpCol = "gdp per capita (current us$)";
  const ghgCol = "total greenhouse gas emissions excluding lulucf per capita (t co2e/capita)";
  
  const plotData = prospAndSust.map(d => ({
    gdp: +d[gdpCol],
    ghg: +d[ghgCol],
    country: d["country"]
  })); 
  
  // Scales
  const x_scale = d3.scaleLinear() 
    .domain(d3.extent(plotData, d => d.gdp))
    .range([0, innerWidth])
    .nice(); 

  const y_scale = d3.scaleLinear()
    .domain(d3.extent(plotData, d => d.ghg))
    .range([innerHeight, 0]) 
    .nice();

  // Gridlines 
  chart.append("g")
    .attr("class", "grid")
    .attr("transform", `translate(0, ${innerHeight})`)
    .call(d3.axisBottom(x_scale)
      .tickSize(-innerHeight)
      .tickFormat("")
    )
    .call(g => g.selectAll("line").attr("stroke-opacity", 0.1));

  chart.append("g")
    .attr("class", "grid")
    .call(d3.axisLeft(y_scale)
      .tickSize(-innerWidth)
      .tickFormat("")
    )
    .call(g => g.selectAll("line").attr("stroke-opacity", 0.1));

  // Axis
  chart.append("g")
    .attr("transform", `translate(0, ${innerHeight})`)
    .call(d3.axisBottom(x_scale)); 

  chart.append("g")
    .call(d3.axisLeft(y_scale));

  chart.selectAll("circle")
    .data(plotData)
    .enter()
    .append("circle")
      .attr("cx", d => x_scale(d.gdp))
      .attr("cy", d => y_scale(d.ghg))
      .attr("r", 5)
      .style("fill", "steelblue")
      .style("opacity", 0.7);

  // Titles
  svg.append("text")
    .attr("text-anchor", "middle")
    .attr("x", dims.margin_left + innerWidth / 2)
    .attr("y", dims.height - dims.margin_bottom / 2)
    .text("GDP Per Capita (Current US$)");

  svg.append("text")
    .attr("text-anchor", "middle")
    .attr("transform", "rotate(-90)")
    .attr("y", dims.margin_left / 2)
    .attr("x", -(dims.margin_top + innerHeight / 2))
    .text("Total Greenhouse Gas Emissions (t CO2e/capita)");

  svg.append("text")
    .attr("text-anchor", "middle")
    .attr("x", dims.width / 2)
    .attr("y", dims.margin_top / 2)
    .style("font-size", "18px")
    .style("font-weight", "bold")
    .text("GDP vs. Greenhouse Gas Emissions");

  return svg.node();
}
```

```js echo
// GDP per capita vs total renewable energy consump
vl.markCircle() 
  .data(prospAndSust)
  .encode(
    vl.x().fieldQ("gdp per capita (current us$)"),
    vl.y().fieldQ("renewable energy consumption (% of total final energy consumption)"),
    vl.tooltip().fieldN("country")
  )
.render(); 
```

```js echo
// GDP Per Capita vs Renewable Energy Use
{
  const dims = {
    width: 810,  
    height: 620,  
    margin_top: 60,
    margin_right: 30,
    margin_bottom: 60,
    margin_left: 80
  };

  const innerWidth = dims.width - dims.margin_left - dims.margin_right;
  const innerHeight = dims.height - dims.margin_top - dims.margin_bottom;

  const svg = d3.create('svg')
    .attr('width', dims.width)
    .attr('height', dims.height);

  const chart = svg.append('g')
    .attr('transform', `translate(${dims.margin_left}, ${dims.margin_top})`);
    
  const gdpCol = "gdp per capita (current us$)";
  const renewableCol = "renewable energy consumption (% of total final energy consumption)";
  
  const plotData = prospAndSust.map(d => ({
    gdp: +d[gdpCol],
    renewable: +d[renewableCol],
    country: d["country"]
  })).filter(d => 
    d.gdp > 0 && typeof d.renewable === 'number' && d.country
  );
  
  // Scales
  const x_scale = d3.scaleLog() 
    .domain(d3.extent(plotData, d => d.gdp))
    .range([0, innerWidth])
    .nice();

  const y_scale = d3.scaleLinear()
    .domain(d3.extent(plotData, d => d.renewable))
    .range([innerHeight, 0]) 
    .nice(); 

  // Gridlines
  chart.append("g")
    .attr("class", "grid")
    .attr("transform", `translate(0, ${innerHeight})`)
    .call(d3.axisBottom(x_scale)
      .tickSize(-innerHeight)
      .tickFormat("")
    )
    .call(g => g.selectAll("line").attr("stroke-opacity", 0.1));

  chart.append("g")
    .attr("class", "grid")
    .call(d3.axisLeft(y_scale)
      .tickSize(-innerWidth)
      .tickFormat("") 
    )
    .call(g => g.selectAll("line").attr("stroke-opacity", 0.1));

  chart.append("g")
    .attr("transform", `translate(0, ${innerHeight})`) 
    .call(d3.axisBottom(x_scale).ticks(5, ".1s"));

  chart.append("g")
    .call(d3.axisLeft(y_scale));

  chart.selectAll("circle")
    .data(plotData)
    .enter()
    .append("circle")
      .attr("cx", d => x_scale(d.gdp))
      .attr("cy", d => y_scale(d.renewable))
      .attr("r", 5)
      .style("fill", "steelblue")
      .style("opacity", 0.7);

  // Titles
  svg.append("text")
    .attr("text-anchor", "middle")
    .attr("x", dims.margin_left + innerWidth / 2) 
    .attr("y", dims.height - dims.margin_bottom / 2)
    .text("GDP Per Capita (Current US$) - Log Scale");

  svg.append("text")
    .attr("text-anchor", "middle")
    .attr("transform", "rotate(-90)")
    .attr("y", dims.margin_left / 2) 
    .attr("x", -(dims.margin_top + innerHeight / 2)) 
    .text("Renewable Energy Consumption (% of Total)");

  svg.append("text")
    .attr("text-anchor", "middle")
    .attr("x", dims.width / 2) 
    .attr("y", dims.margin_top / 2) 
    .style("font-size", "18px")
    .style("font-weight", "bold")
    .text("GDP vs. Renewable Energy Consumption");

  return svg.node();
}
```

```js echo
vl.markCircle() 
  .data(prospAndSust)
  .transform(
    vl.calculate("toNumber(datum['poverty headcount ratio at $6.85 a day (2017 ppp) (% of population)'])").as("poverty_num"),
    vl.calculate("toNumber(datum['pm2.5 air pollution, mean annual exposure (micrograms per cubic meter)'])").as("air_pollution_num")
  )
  .encode(
    vl.x().fieldQ("poverty_num"),
    vl.y().fieldQ("air_pollution_num")
    )
.render(); 
```

```js echo
// Poverty vs. Air Pollution
{
  // Chart setup
  const dims = {
    width: 810,    
    height: 620,  
    margin_top: 60,
    margin_right: 30,
    margin_bottom: 60,
    margin_left: 80
  };

  const innerWidth = dims.width - dims.margin_left - dims.margin_right;
  const innerHeight = dims.height - dims.margin_top - dims.margin_bottom;

  const svg = d3.create('svg')
    .attr('width', dims.width)
    .attr('height', dims.height);

  const chart = svg.append('g')
    .attr('transform', `translate(${dims.margin_left}, ${dims.margin_top})`);
    
  const povertyCol = "poverty headcount ratio at $6.85 a day (2017 ppp) (% of population)";
  const pollutionCol = "pm2.5 air pollution, mean annual exposure (micrograms per cubic meter)";
  
  const plotData = prospAndSust.map(d => ({
    poverty: +d[povertyCol],
    pollution: +d[pollutionCol],
    country: d["country"]
  })).filter(d => 
    !isNaN(d.poverty) && !isNaN(d.pollution) && d.country
  );
  
  // Scales
  const x_scale = d3.scaleLinear() 
    .domain(d3.extent(plotData, d => d.poverty))
    .range([0, innerWidth])
    .nice(); 
  
  const y_scale = d3.scaleLinear()
    .domain(d3.extent(plotData, d => d.pollution))
    .range([innerHeight, 0]) 
    .nice(); 

  // Gridlines
  chart.append("g")
    .attr("class", "grid")
    .attr("transform", `translate(0, ${innerHeight})`)
    .call(d3.axisBottom(x_scale)
      .tickSize(-innerHeight)
      .tickFormat("") 
    )
    .call(g => g.selectAll("line").attr("stroke-opacity", 0.1));

  chart.append("g")
    .attr("class", "grid")
    .call(d3.axisLeft(y_scale)
      .tickSize(-innerWidth)
      .tickFormat("") 
    )
    .call(g => g.selectAll("line").attr("stroke-opacity", 0.1));

  // Axes
  chart.append("g")
    .attr("transform", `translate(0, ${innerHeight})`) 
    .call(d3.axisBottom(x_scale));

  chart.append("g")
    .call(d3.axisLeft(y_scale));

  chart.selectAll("circle")
    .data(plotData)
    .enter()
    .append("circle")
      .attr("cx", d => x_scale(d.poverty))
      .attr("cy", d => y_scale(d.pollution))
      .attr("r", 5)
      .style("fill", "steelblue")
      .style("opacity", 0.7);

  // Titles
  svg.append("text")
    .attr("text-anchor", "middle")
    .attr("x", dims.margin_left + innerWidth / 2) 
    .attr("y", dims.height - dims.margin_bottom / 2)
    .text("Poverty Headcount at $6.85/day (% of Population)");

  svg.append("text")
    .attr("text-anchor", "middle")
    .attr("transform", "rotate(-90)")
    .attr("y", dims.margin_left / 2)
    .attr("x", -(dims.margin_top + innerHeight / 2))
    .text("PM2.5 Air Pollution (Micrograms per Cubic Meter)");
  
  svg.append("text")
    .attr("text-anchor", "middle")
    .attr("x", dims.width / 2) 
    .attr("y", dims.margin_top / 2)
    .style("font-size", "18px")
    .style("font-weight", "bold")
    .text("Poverty vs. Air Pollution");

  return svg.node();
}
```

The domain question was asking which regions showed the strongest balance between economic prosperity and sustainability. The first two visualizations directly showed how a country's GDP may affect their sustainability efforts through their total greenhouse gas emissions and how much renewable energy they use. Ideally, in the first visualization, the countries with a higher GDP will also have a lower total greenhouse gas emission. However, as countries develop, the factories they create may not be the most environmentally friendly. In the second visualization, we had originally expected the countries with a higher GDP to have a higher renewable energy consumption. However, what ended up being shown is that the countries with a lower GDP have a higher rate of using renewable energy. 
The last visualization shows the correlation between poverty and air pollution. Unfortunately, we could not distinguish a specific pattern in this visualization. In the future, we will add tooltips to show which countries are represented by which dot. 

Domain Question #6

```table echo

```

```js echo
gapCsv = FileAttachment("education_health_gap_data.csv").csv(); 
```

```js echo
// Education Line Chart
{
  // Chart Set Up
  const dims = {
    width: 810,   
    height: 620,  
    margin_top: 60,
    margin_right: 150,
    margin_bottom: 60,
    margin_left: 80
  };

  const innerWidth = dims.width - dims.margin_left - dims.margin_right;
  const innerHeight = dims.height - dims.margin_top - dims.margin_bottom;

  const svg = d3.create('svg')
    .attr('width', dims.width)
    .attr('height', dims.height);

  const chart = svg.append('g')
    .attr('transform', `translate(${dims.margin_left}, ${dims.margin_top})`);
    
  // Groups
  const highIncomeCountries = new Set([
    "USA", "DEU", "JPN", "GBR", "CAN", "FRA", "AUS", "NOR", "SWE"
  ]);

  const developingCountries = new Set([
    "BRA", "RUS", "IND", "CHN", "ZAF",
    "NGA", "PAK", "BGD", "MEX", "IDN", "ETH", "EGY"
  ]);

  function assignGroup(country) {
    if (highIncomeCountries.has(country)) {
      return "High-Income";
    }
    if (developingCountries.has(country)) {
      return "Developing";
    }
    return null;
  }

  const metricCol = "primary completion rate, total (% of relevant age group)";
  
  const processedData = gapCsv.map(d => ({
    year: d3.timeParse("%Y")(d.year), 
    group: assignGroup(d.country),
    value: +d[metricCol]
  })).filter(d => 
    d.group && !isNaN(d.value) && d.year
  );
  
  const avgData = d3.rollup(
    processedData,
    v => d3.mean(v, d => d.value), 
    d => d.year,                   
    d => d.group                 
  );
  
  const flatData = [];
  for (const [year, groups] of avgData) {
    for (const [group, value] of groups) {
      flatData.push({ year, group, value });
    }
  }

  // Scales
  const x_scale = d3.scaleTime()
    .domain(d3.extent(flatData, d => d.year))
    .range([0, innerWidth])
    .nice();

  const y_scale = d3.scaleLinear()
    .domain([0, 100])
    .range([innerHeight, 0])
    .nice();
    
  const colorScale = d3.scaleOrdinal()
    .domain(["High-Income", "Developing"])
    .range(d3.schemeTableau10); 

  // Axes
  chart.append("g")
    .attr("transform", `translate(0, ${innerHeight})`)
    .call(d3.axisBottom(x_scale));

  chart.append("g")
    .call(d3.axisLeft(y_scale).ticks(10, "%")); 

  // Line ---------------------
  const lineGenerator = d3.line()
    .x(d => x_scale(d.year))
    .y(d => y_scale(d.value))
    .curve(d3.curveMonotoneX); 
    
  const groupedForLines = d3.group(flatData, d => d.group);

  chart.selectAll(".line-path")
    .data(groupedForLines)
    .enter()
    .append("path")
      .attr("class", "line-path")
      .attr("d", d => lineGenerator(d[1].sort((a, b) => a.year - b.year))) // d[1] is the array of data
      .style("fill", "none")
      .style("stroke", d => colorScale(d[0])) // d[0] is the group name
      .style("stroke-width", 3);

  // Legend -----------
  const legend = svg.append("g")
    .attr("transform", `translate(${dims.margin_left + innerWidth + 20}, ${dims.margin_top})`);
    
  colorScale.domain().forEach((group, i) => {
    const legendRow = legend.append("g")
      .attr("transform", `translate(0, ${i * 25})`);
      
    legendRow.append("rect")
      .attr("width", 20)
      .attr("height", 20)
      .attr("fill", colorScale(group));
      
    legendRow.append("text")
      .attr("x", 30)
      .attr("y", 15)
      .text(group);
  });

  // Titles
  svg.append("text")
    .attr("text-anchor", "middle")
    .attr("x", dims.width / 2)
    .attr("y", dims.margin_top / 2)
    .style("font-size", "18px")
    .style("font-weight", "bold")
    .text("Education Gap: High-Income vs. Developing Nations");

  svg.append("text")
    .attr("text-anchor", "middle")
    .attr("x", dims.margin_left + innerWidth / 2)
    .attr("y", dims.height - dims.margin_bottom / 2)
    .text("Year");

  svg.append("text")
    .attr("text-anchor", "middle")
    .attr("transform", "rotate(-90)")
    .attr("y", dims.margin_left / 2)
    .attr("x", -(dims.margin_top + innerHeight / 2))
    .text("Primary Completion Rate (%)");

  return svg.node();
}
```

Q: Have developing countries narrowed the gap with high-income nations in education and health outcomes?

This chart shows the completion rate of primary school education with two lines. The blue line represents the high income countries and orange line represents developing countries. What is shown in the graph is that at one point, the developing countries had a higher primary completion rate than developing countries and later on, they became almost equal. This shows that the gap between developing and high income countries is decreasing and shows the foundations of the education field in developing countries is quickly increasing. 

Domain Question #8 Can we identify clusters of countries with similar socio-economic profiles using visualization (e.g., scatterplots or map visualizations)

```table echo

```

```js echo
socioeco = FileAttachment("socioeconomic_profiles.csv").csv(); 
```

```js echo
vl.markCircle() 
  .data(socioeco) 
  .encode(
    vl.x().fieldQ("gdp per capita (current us$)"),
    vl.y().fieldQ("literacy rate, adult total (% of people ages 15 and above)"), 
  )
.render();
```

For this domain question, we are planning to use a clustering algorithm to see if we can group the countries with similar socioeconomic profiles together. Following this, we will put this data on a choropleth to visualize the clusters
