def generate_insights(df):
    insights = []

    for col in df.select_dtypes(include='number'):
        insights.append(
            f"The average value of {col} is {df[col].mean():.2f}."
        )
        insights.append(
            f"The maximum value of {col} is {df[col].max()}."
        )

    return insights
