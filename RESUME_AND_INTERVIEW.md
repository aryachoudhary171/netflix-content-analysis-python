# Resume and Interview Notes

## Resume bullets
- Cleaned and analyzed **8,807 Netflix titles** with Python and Pandas, documenting missing metadata, date parsing, duration parsing, and source-field repair.
- Used Matplotlib and Seaborn to analyze catalog composition; found that Movies account for **69.6%** of titles and the peak recorded addition year was **2019** (2,016 titles).
- Created separate exploded country, genre, director, and cast datasets; identified **International Movies** (2,752 titles) and **United States** (3,690) as the leading genre and country.

## LinkedIn draft
I completed a Python data analysis project on the Netflix Movies and TV Shows catalog using Pandas, Matplotlib, and Seaborn. This snapshot contains 8,807 titles, including 69.6% Movies. I explored additions over time, countries, genres, ratings, and runtimes, and built a documented cleaning workflow with exploded tables for multi-value metadata. The dataset has no viewing data, so these findings describe catalog records rather than popularity.

#DataAnalytics #Python #Pandas #PortfolioProject

## Interview questions and short answers
1. **Why this project?** It demonstrates an end-to-end workflow from raw CSV inspection through cleaning, analysis, charts, and communication.
2. **Why keep the raw file unchanged?** It preserves a reproducible source and lets us rerun cleaning.
3. **Why fill director/cast/country with Unknown?** Dropping those rows would remove valid titles; the label keeps missing metadata visible.
4. **Why explode country and genre?** A title with several values should count once in each represented dimension. Use unique `show_id` to avoid overcounting.
5. **How did you handle date conversion?** `pd.to_datetime(..., errors="coerce")` parses valid dates and leaves invalid/missing values empty; year/month fields are derived afterward.
6. **How did you detect ratings that were actually durations?** A regular expression checks for a number followed by `min` in rating; the cleaner moves those values to duration and clears the bad rating.
7. **Why group ratings?** Broad groups are easier to interpret; values outside the documented mapping remain Not Rated.
8. **What is the mean/median difference for movie duration?** The mean uses all runtimes and is pulled by extremes; the median is the middle value and is more robust to skew.
9. **What is content age?** Addition year minus release year, an approximate gap based on recorded date metadata.
10. **What does an addition trend show?** It counts recorded additions in this snapshot, not acquisitions or audience demand across the full service.
11. **How do you avoid overcounting?** Count unique `show_id` within exploded dimensions.
12. **Why Pandas and Seaborn/Matplotlib?** Pandas handles cleaning and aggregation; Matplotlib/Seaborn create readable charts.
13. **What are the main limitations?** There are no views, revenue, licensing costs, user ratings, or reliable current availability data.
14. **What would you improve with more data?** Join reliable viewing, cost, and audience data and examine whether catalog mix relates to outcomes.
15. **What would you do next?** Validate findings with stakeholders, add data-quality checks, and build a Power BI dashboard if interactive reporting is needed.

## Before publishing
Review the charts and code, and practice explaining each cleaning choice in your own words. The project describes catalog records, not popularity or performance.
