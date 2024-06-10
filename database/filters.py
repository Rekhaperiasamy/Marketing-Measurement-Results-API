class Filters:
    def get_marketing_data_filter(
            table: str,
            product: str = None,
            campaign_type: str = None,
            campaign: str = None,
            channel: str = None,
            start_date: str = None,
            end_date: str = None):

        filters = []

        if channel:
            channels = [x.strip() for x in channel.split(',')]
            filters.append(table.channel.in_(channels))

        if product:
            products = [x.strip() for x in product.split(',')]
            filters.append(table.product.in_(products))

        if campaign:
            campaigns = [x.strip() for x in campaign.split(',')]
            filters.append(table.campaign.in_(campaigns))

        if campaign_type:
            campaign_types = [x.strip() for x in campaign_type.split(',')]
            filters.append(table.campaign_type.in_(campaign_types))

        if start_date and end_date:
            filters.append(table.date.between(start_date, end_date))

        return filters
