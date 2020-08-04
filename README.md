# Risk-Analysis-on-Taiwanese-Companies

In this project, we aim to provide a system that could perform risk analysis to companies based on:

* Accounting Information
* Industrial Prospective
* Company Reputation
* Company Relationships

To be more accurate, we design our system to have the ability to
1. Analyze the financial report and extract important informations
2. Perform social media monitering and analysis on certain companies and industries
3. Build graph database for companies and products and infer relationships on it

## System Overview
The image below shows the overview of our system. 

<img src="readme_images/overview.png">

Our model can be split into three parts:

### Financial reports

| Category           | Variable | Ratios                                    |
|--------------------|----------|-------------------------------------------|
| Firm size          | Z1       | Total asset value                         |
|                    | Z4       | Book-to-market value                      |
| Financial leverage | Z5       | long-term debts / total invested capital  |
|                    | Z7       | Total debt / total capital                |
| Profitability      | Z11      | Operating income / received capitals      |
|                    | Z13      | Net income before tax / received capitals |
|                    | Z15      | Gross profit margin                       |
|                    | Z17      | Earnings per share (EPS)                  |
| Liquidity          | Z22      | Quick Ratio                               |

## Webpage Visualization
For model comparing
```
python main.py compare [model] [method]
```
Available models: MLP, Forest, SVM, XGB, MLP <br>
Available methods: player, team

For prediction
```
python main.py predict
```
For clustering
```
python main.py cluster
```

## Contributors
This project is also contributed by Pei-Ling Tsai (pt2534@columbia.edu).
