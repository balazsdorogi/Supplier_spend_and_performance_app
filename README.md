# Supplier_spend_and_performance_app
 Interactive dashboard built with Dash to evaluate spendings with suppliers and delivery performance for supply chain management companies. 

First tab: Supplier Spend
    <br>&nbsp;&nbsp;Chart 1 (area chart): Comparison of purchase costs in 2018 and 2019 by supplier - supplier can be selected from the dropdown (interactive)
    <br>&nbsp;&nbsp;Chart 2 (area chart): Comparison of total purchase costs in 2018 and 2019
    <br>&nbsp;&nbsp;Chart 3 (pie chart): Comparison of purchase costs in 2018 and 2019 with percentage of spendings with each supplier shown - suppliers have the same colours in both years, so any changes in procurement can be tracked
<br><br>
Second tab: Supplier Deliveries
    <br>&nbsp;&nbsp;Chart 1: (line chart): Showing if deliveries from suppliers arrived on-time in 2019 - supplier can be selected from the dropdown (interactive)
    <br>&nbsp;&nbsp;Chart 2: (line chart): Showing if deliveries from suppliers arrived on-time in 2018 - supplier can be selected from the dropdown (interactive)
    <br>&nbsp;&nbsp;The second tab has two dropdowns, so different entities from the same company can be compared. To help interpret the EKG chart, the y-axis has a (-) and a (+) symbol after Early and Late respectively. Even though I called it an EKG chart, a very good supplier would have a completely flat line that crosses the y-axes at 0, meaning they always deliver on-time (the difference between their promised day and the receipt date is 0). Time is measured in days, so a value of -2 means a delivery was 2 days early, while +4 tells us it was 4 days late.
    <br>&nbsp;&nbsp;Why do we even track early deliveries? Even though these are much better than late ones, they can still create an issue when it comes to warehouse management, so it's best to keep track of them in case further discussions will be needed with specific suppliers about delivery management.
