class Helper:

    def get_status(level):

        status_map = {
            0: "Пользователь",
            1: "Поддержка",
            2: "Админ",
            3: "???"
        }

        status = status_map.get(level)

        return status
    