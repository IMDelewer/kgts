class Helper():

    def get_status(level):

        status_map = {
            0: "Пользователь",
            1: "Покупатель",
            2: "Админ",
            3: "RainBS",
            4: "???"
        }

        status = status_map.get(level)

        return status
    