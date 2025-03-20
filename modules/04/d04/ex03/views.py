from django.shortcuts import render


def gradient_table(request):
    colors = {"black": (0, 0, 0), "red": (255, 0, 0), "blue": (0, 0, 255), "green": (0, 255, 0)}

    gradient_data = []
    for i in range(50):
        row = []
        for color, (r, g, b) in colors.items():
            # scale from 0 to 255 over 50 levels
            factor = int((i / 49) * 255)
            row.append(f"{factor * r // 255}, {factor * g // 255}, {factor * b // 255}")
        gradient_data.append(row)

    return render(request, "ex03/index.html", {"gradient_data": gradient_data})
