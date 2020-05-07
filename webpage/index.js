var chart = {
  const svg = d3.create("svg")
      .attr("viewBox", [0, 0, width, height]);

  svg.append("g")
    .selectAll("g")
    .data(series)
    .join("g")
      .attr("fill", d => color(d.key))
    .selectAll("rect")
    .data(d => d.map(v => Object.assign(v, {key: d.key})))
    .join("rect")
      .attr("x", d => x(d[0]))
      .attr("y", ({data: [name]}) => y(name))
      .attr("width", d => x(d[1]) - x(d[0]))
      .attr("height", y.bandwidth())
    .append("title")
      .text(({key, data: [name, value]}) => `${name} ${formatValue(value.get(key))} ${key}`);

  svg.append("g")
      .call(xAxis);

  svg.append("g")
      .call(yAxis);

  return svg.node();
}

var data = {
  const categories = {
    "pants-fire": "Pants on fire!",
    "false": "False",
    "mostly-false": "Mostly false",
    "barely-true": "Mostly false", // recategorized
    "half-true": "Half true",
    "mostly-true": "Mostly true",
    "true": "True"
  };

  const data = d3.csvParse(await FileAttachment("politifact.csv").text(), ({speaker: name, ruling: category, count: value}) => categories[category] ? {name, category: categories[category], value: +value} : null);

  // Normalize absolute values to percentage.
  d3.rollup(data, group => {
    const sum = d3.sum(group, d => d.value);
    for (const d of group) d.value /= sum;
  }, d => d.name);

  return Object.assign(data, {
    format: ".0%",
    negative: "← More falsehoods",
    positive: "More truths →",
    negatives: ["Pants on fire!", "False", "Mostly false"],
    positives: ["Half true", "Mostly true", "True"]
  });
}

signs = new Map([].concat(
  data.negatives.map(d => [d, -1]),
  data.positives.map(d => [d, +1])
))

bias = d3.rollups(data, v => d3.sum(v, d => d.value * Math.min(0, signs.get(d.category))), d => d.name)
  .sort(([, a], [, b]) => d3.ascending(a, b))

series = d3.stack()
    .keys([].concat(data.negatives.slice().reverse(), data.positives))
    .value(([, value], category) => signs.get(category) * (value.get(category) || 0))
    .offset(d3.stackOffsetDiverging)
  (d3.rollups(data, data => d3.rollup(data, ([d]) => d.value, d => d.category), d => d.name))

x = d3.scaleLinear()
    .domain(d3.extent(series.flat(2)))
    .rangeRound([margin.left, width - margin.right])

y = d3.scaleBand()
    .domain(bias.map(([name]) => name))
    .rangeRound([margin.top, height - margin.bottom])
    .padding(2 / 33)

color = d3.scaleOrdinal()
    .domain([].concat(data.negatives, data.positives))
    .range(d3.schemeSpectral[data.negatives.length + data.positives.length])


xAxis = g => g
    .attr("transform", `translate(0,${margin.top})`)
    .call(d3.axisTop(x)
        .ticks(width / 80)
        .tickFormat(formatValue)
        .tickSizeOuter(0))
    .call(g => g.select(".domain").remove())
    .call(g => g.append("text")
        .attr("x", x(0) + 20)
        .attr("y", -24)
        .attr("fill", "currentColor")
        .attr("text-anchor", "start")
        .text(data.positive))
    .call(g => g.append("text")
        .attr("x", x(0) - 20)
        .attr("y", -24)
        .attr("fill", "currentColor")
        .attr("text-anchor", "end")
        .text(data.negative))

yAxis = g => g
    .call(d3.axisLeft(y).tickSizeOuter(0))
    .call(g => g.selectAll(".tick").data(bias).attr("transform", ([name, min]) => `translate(${x(min)},${y(name) + y.bandwidth() / 2})`))
    .call(g => g.select(".domain").attr("transform", `translate(${x(0)},0)`))

formatValue = {
  const format = d3.format(data.format || "");
  return x => format(Math.abs(x));
}

height = bias.length * 33 + margin.top + margin.bottom

margin = ({top: 40, right: 30, bottom: 0, left: 80})

d3 = require("d3@5", "d3-array@2")

import {swatches} from "@d3/color-legend"