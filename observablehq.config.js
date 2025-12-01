// See https://observablehq.com/framework/config for documentation.
export default {
  // The app’s title; used in the sidebar and webpage titles.
  title: "Plot Of Gold",

  // The pages and sections in the sidebar. If you don’t specify this option,
  // all pages will be listed in alphabetical order. Listing pages explicitly
  // lets you organize them into sections and have unlisted pages.
  pages: [
    {
      name: "Introduction",
      path: "/index"
    },
    {
      name: "How have GDP per capita and life expectancy evolved across income groups since 1990?",
      path: "/q1"
    },
    {
      name: "Is there a visible correlation between economic growth and social progress (e.g., life expectancy, literacy rate), and do countries with similar GDP levels differ in their social performance?",
      path: "/q2"
    },
    {
      name: "Do higher-income countries have lower poverty rates?",
      path: "/q3"
    },
    {
      name: "Is there a trade-off between economic growth and CO₂ emissions?",
      path: "/q4"
    },
    ...(process.env.NODE_ENV !== "production" ? [
      {
        name: "Converted",
        path: "/converted",
        hidden: true
      }
    ] : []),
  ],
  // Content to add to the head of the page, e.g. for a favicon:
  head: `
  <link rel="stylesheet" href="custom-styles.css">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
`,

  // The path to the source root.
  root: "src",
  // Some additional configuration options and their defaults:
  theme: "deep-space", // try "light", "dark", "slate", etc.
  // header: "", // what to show in the header (HTML)
  // footer: "Built with Observable.", // what to show in the footer (HTML)
  // sidebar: true, // whether to show the sidebar
  // toc: true, // whether to show the table of contents
  // pager: true, // whether to show previous & next links in the footer
  // output: "dist", // path to the output root for build
  // search: true, // activate search
  // linkify: true, // convert URLs in Markdown to links
  // typographer: false, // smart quotes and other typographic improvements
  // preserveExtension: false, // drop .html from URLs
  // preserveIndex: false, // drop /index from URLs
};
