import matplotlib.pyplot as plt
from datetime import timedelta
import pandas as pd
def generate_chart(df, current_date):
    days_ago = current_date - timedelta(days=31)
    df['Date'] = pd.to_datetime(df['Date'])
    filtered_df = df[df['Date'] >= days_ago]
    dates = filtered_df['Date'].to_list()
    antreaja = filtered_df['AntreAja'].to_list()
    chatgpt = filtered_df['ChatGPT'].to_list()
    indihome = filtered_df['Indihome'].to_list()
    kartu_sim = filtered_df['Kartu SIM'].to_list()
    roaming = filtered_df['Roaming'].to_list()
    telkomsel_one = filtered_df['Telkomsel One'].to_list()
    plt.rcParams['figure.figsize'] = [16, 10]
    plt.rcParams['figure.autolayout'] = True
    # fig = plt.figure()
    plt.plot(dates, antreaja, linestyle="-", marker='o', label='AntreAja')
    # ax = fig.add_subplot(111)
    plt.margins(x=0, y=0)

    max_value = 0

    max_value = max(antreaja) if max(antreaja) > max_value else max_value
    max_value = max(chatgpt) if max(chatgpt) > max_value else max_value
    max_value = max(indihome) if max(indihome) > max_value else max_value
    max_value = max(roaming) if max(roaming) > max_value else max_value
    max_value = max(telkomsel_one) if max(telkomsel_one) > max_value else max_value
    max_value += 20

    modifier = 10
    index = 0
    if max_value <= 40:
        modifier = 5
    elif max_value > 40:
        modifier = 10
    elif max_value > 199:
        index = 100
        modifier = 20
    elif max_value > 399:
        index = 100
        modifier = 50
    elif max_value >= 500:
        index = 100
        modifier = 100

    x_ticks = []
    while index <= max_value:
        x_ticks.append(index)
        index += modifier

    # Plotting the second line
    plt.plot(dates, chatgpt, label='ChatGPT', linestyle='-', marker='o', color='red')  # Customizing linestyle and color
    plt.plot(dates, indihome, label='Indihome', linestyle='-', marker='o', color='green')  # Customizing linestyle and color
    plt.plot(dates, kartu_sim, label='Kartu SIM', linestyle='-', marker='o', color='purple')  # Customizing linestyle and color
    plt.plot(dates, roaming, label='Roaming', linestyle='-', marker='o', color='skyblue')  # Customizing linestyle and color
    plt.plot(dates, telkomsel_one, label='Telkomsel One', linestyle='-', marker='o', color='orange')  # Customizing linestyle and color
    # plt.plot(x_values, y_values3, label='Line 3', linestyle='-', color='green')  # Customizing linestyle and color

    # Adding labels and title
    # plt.xlabel('Date')
    plt.xticks(dates, rotation=90)
    plt.yticks(x_ticks)
    plt.ylabel('')
    plt.title('Vedita Daily Report')

    for x, y1, y2, y3, y4, y5, y6 in zip(dates, antreaja, chatgpt, indihome, kartu_sim, roaming, telkomsel_one):
        plt.text(x, y1 + 0.4, f'{y1}', ha='center', va='bottom')
        plt.text(x, y2 + 0.4, f'{y2}', ha='center', va='bottom')
        plt.text(x, y3 + 0.4, f'{y3}', ha='center', va='bottom')
        plt.text(x, y4 + 0.4, f'{y4}', ha='center', va='bottom')
        plt.text(x, y5 + 0.4, f'{y5}', ha='center', va='bottom')
        plt.text(x, y6 + 0.4, f'{y6}', ha='center', va='bottom')

    # Adding a legend
    plt.legend()

    # Display the chart
    plt.grid(True, axis='y')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    # plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.18), ncol=6)  # Adjust the bbox_to_anchor as needed
    plt.subplots_adjust(bottom=0.3)
    plt.tight_layout()
    filename = "./my_chart.jpg"
    plt.savefig(filename, bbox_inches='tight')
    # plt.show()
    return filename