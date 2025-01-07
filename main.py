import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://localhost:9000"

state_mapping = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
    "New York": "NY", "North Carolina": "NC", "North Dakota": "ND",
    "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
    "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
    "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY"
}


@st.cache_data(ttl=300)
def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_URL}{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None


st.set_page_config(layout="wide")
st.title("Dashboard des Ventes Ecommerce")

page = st.sidebar.selectbox("Choisir une analyse",
                            ["Analyse Générale", "Analyse Produits", "Analyse par Ville", "Ventes par État",
                             "Ventes par produit", "Ventes par Mois"])

if page == "Analyse Produits":
    st.header("Analyse des Ventes par Produit")

    product_sales_data = fetch_data("/ecommerce/sales-by-product")
    if product_sales_data:
        df = pd.DataFrame(product_sales_data["sales_by_product"])
        if not df.empty:

            fig = px.bar(df, x="_id", y="totalSales", title="Ventes par Produit",
                         labels={"_id": "Nom du Produit", "totalSales": "Ventes Totales"})
            st.plotly_chart(fig)

            top_product = df.loc[df['totalSales'].idxmax()]
            st.write(f"Produit le plus vendu : {top_product['_id']} ({top_product['totalSales']:.2f} $)")

            bottom_product = df.loc[df['totalSales'].idxmin()]
            st.write(f"Produit le moins vendu : {bottom_product['_id']} ({bottom_product['totalSales']:.2f} $)")

            # Afficher uniquement les 5 produits les moins vendus
            st.subheader("Top 5 des Produits les Moins Vendus")
            bottom_5_products = df.nsmallest(5, "totalSales")
            st.table(bottom_5_products[["_id", "totalSales"]])

            # Nombre de produits différents
            st.write(f"Nombre de produits différents : {len(df)}")

            st.subheader("Filtrer par Produit")
            selected_product = st.selectbox("Choisir un produit", options=df["_id"].unique())

            if selected_product:
                product_data = df[df["_id"] == selected_product]
                total_sales = product_data["totalSales"].iloc[0]
                st.write(f"Ventes totales pour **{selected_product}** : {total_sales:.2f} $")

                sales_by_post_code_data = fetch_data("/ecommerce/sales-by-post-code")
                if sales_by_post_code_data:
                    df_post_code = pd.DataFrame(sales_by_post_code_data["sales_by_code_post"])
                    if not df_post_code.empty:
                        num_cities = len(df_post_code["_id"].unique())
                        st.write(f"Nombre de villes différentes où **{selected_product}** a été vendu : {num_cities}")
                    else:
                        st.write("Aucune donnée disponible pour les villes.")
        else:
            st.write("Aucune donnée disponible pour les ventes par produit.")
    else:
        st.write("Erreur dans la récupération des données des ventes par produit.")

elif page == "Analyse Générale":
    st.header("Analyse Générale des Ventes")

    total_sales_data = fetch_data("/ecommerce/total-sales")
    total_orders_data = fetch_data("/ecommerce/total-orders")
    average_sales_data = fetch_data("/ecommerce/average-cart")
    ship_mode_data = fetch_data("/ecommerce/sales-by-ship-mode")

    if total_sales_data and total_orders_data and average_sales_data:
        if isinstance(total_sales_data.get('total des ventes'), list):
            total_sales = total_sales_data['total des ventes'][0].get('total_sales', 0)
        else:
            total_sales = total_sales_data.get('total_sales', 0)
        total_orders = total_orders_data.get("total_orders", 0)
        if isinstance(average_sales_data.get("panier moyen"), list):
            average_sales = average_sales_data["panier moyen"][0].get('average_basket', 0)
        else:
            average_sales = average_sales_data.get("panier moyen", 0)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Ventes Totales", value=f"${total_sales:,.2f}")
        with col2:
            st.metric(label="Total Commandes", value=total_orders)
        with col3:
            st.metric(label="Panier Moyen", value=f"${average_sales:,.2f}")

    if ship_mode_data:
        df_ship_mode = pd.DataFrame(ship_mode_data["sales_by_ship_mode"])
        if not df_ship_mode.empty:
            fig_ship_mode = px.pie(df_ship_mode, names="_id", values="totalSales",
                                   title="Répartition des Ventes par Mode de Livraison")
            st.plotly_chart(fig_ship_mode)
        else:
            st.write("Aucune donnée disponible pour les modes de livraison.")

if page == "Analyse par Ville":
    st.header("Analyse des Ventes par Ville")

    # Récupération des données
    sales_by_city_data = fetch_data("/ecommerce/sales-by-city")

    if sales_by_city_data and "sales_by_city" in sales_by_city_data:
        df_city_sales = pd.DataFrame(sales_by_city_data["sales_by_city"])

        if not df_city_sales.empty:
            df_city_sales.rename(columns={"_id": "Ville", "totalSales": "Ventes Totales"}, inplace=True)

            # Statistiques descriptives des ventes par ville
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Top 5 des villes avec le plus de ventes")
                top_5_cities = df_city_sales.nlargest(5, "Ventes Totales")
                st.table(top_5_cities)

            with col2:
                st.subheader("Top 5 des villes avec le moins de ventes")
                bottom_5_cities = df_city_sales.nsmallest(5, "Ventes Totales")
                st.table(bottom_5_cities)

            # Graphique des ventes par ville
            st.subheader("Graphique des Ventes par Ville")
            fig_city_sales = px.bar(
                df_city_sales,
                x="Ville",
                y="Ventes Totales",
                color="Ventes Totales",
                title="Ventes Totales par Ville",
                labels={"Ville": "Nom de la Ville", "Ventes Totales": "Ventes Totales (en $)"},
            )
            fig_city_sales.update_layout(
                xaxis_title="Ville",
                yaxis_title="Ventes Totales ($)",
                margin=dict(l=40, r=40, t=40, b=40),
                template="plotly_white",
            )
            st.plotly_chart(fig_city_sales, use_container_width=True)

            # Aperçu des données
            st.subheader("Aperçu des Données")
            st.dataframe(df_city_sales.sort_values("Ventes Totales", ascending=False))

        else:
            st.warning("Aucune donnée disponible pour les ventes par ville.")
    else:
        st.error("Erreur lors de la récupération des données des ventes par ville.")

elif page == "Ventes par État":
    st.subheader("🌍 Ventes par État")

    # Récupération des données
    state_data = fetch_data("/ecommerce/sales-by-state")

    if state_data and "sales_by_state" in state_data:
        df_state = pd.DataFrame(state_data["sales_by_state"])

        if not df_state.empty:
            # Convertir les états en codes d'état
            df_state = df_state.copy()  # Créer une copie pour éviter les warnings
            df_state["state_code"] = df_state["State"].map(state_mapping)

            # Carte choroplèthe pour les ventes par état
            fig = px.choropleth(
                df_state,
                locations="state_code",
                locationmode="USA-states",
                color="Total Sales",
                color_continuous_scale=["#FFEB3B", "#FFA726", "#FF5722", "#D32F2F"],  # Du jaune au rouge
                scope="usa",
                title="Ventes par État",
                labels={"Total Sales": "Ventes Totales ($)"}
            )

            # Personnalisation supplémentaire de la figure
            fig.update_layout(
                geo_scope='usa',
                margin=dict(l=0, r=0, t=30, b=0),
                # Personnalisation de la barre de couleur
                coloraxis_colorbar=dict(
                    title="Ventes ($)",
                    tickformat=",.0f"
                )
            )

            st.plotly_chart(fig)

            # Afficher aussi un tableau des ventes par état
            st.subheader("Détail des ventes par état")
            st.dataframe(
                df_state[["State", "Total Sales"]]
                .sort_values("Total Sales", ascending=False)
                .reset_index(drop=True)
            )

        else:
            st.write("Aucune donnée disponible pour les ventes par état.")
    else:
        st.write("Erreur dans la récupération des données pour les ventes par état.")


elif page == "Ventes par produit":
    st.subheader("Ventes par produit")
    data = fetch_data("/ecommerce/sales-by-product")
    if data:
        df_product = pd.DataFrame(data["sales_by_product"])
        if not df_product.empty:
            top_products = df_product.nlargest(10, "totalSales")
            fig = px.bar(
                top_products,
                x="_id",
                y="totalSales",
                color="totalSales",
                title="Top 10 des ventes par produit",
            )
            st.plotly_chart(fig)
        else:
            st.warning("Aucune donnée disponible pour les ventes par produit.")
    else:
        st.error("Erreur dans la récupération des données.")

elif page == "Ventes par client":
    st.subheader("Ventes par client")
    data = fetch_data("/ecommerce/sales-by-customer")

    # Vérifier si les données existent et contiennent les informations nécessaires
    if data and "sales_by_customer" in data:
        df = pd.DataFrame(data["sales_by_customer"])

        # Vérifier si le DataFrame n'est pas vide
        if not df.empty:
            df = df.rename(
                columns={"_id": "Client ID", "customer_name": "Nom du client", "total_sales": "Ventes totales"})
            top_clients = df.nlargest(10, "Ventes totales")
            fig = px.bar(
                top_clients,
                x="Nom du client",
                y="Ventes totales",
                color="Ventes totales",
                title="Top 10 des ventes par client",
            )
            st.plotly_chart(fig)
            st.dataframe(top_clients)
        else:
            st.warning("Aucune donnée disponible pour les ventes par client.")
    else:
        st.warning("Aucune donnée disponible ou erreur dans la récupération")

if page == "Analyse Produits":
    st.header("Analyse des Ventes par Produit")

    # Récupérer les données des ventes par produit depuis l'API
    product_sales_data = fetch_data("/ecommerce/sales-by-category")

    if product_sales_data:
        df = pd.DataFrame(product_sales_data["sales_by_category"])

        if not df.empty:
            # Graphique en barre pour les ventes par catégorie
            fig_bar = px.bar(
                df,
                x="category",  # Catégorie de produit
                y="total_sales",  # Total des ventes par catégorie
                title="Ventes par Catégorie", labels={"category": "Catégorie", "total_sales": "Ventes Totales (en $)"},
            )
            st.plotly_chart(fig_bar)

            # Graphique en camembert pour la répartition des ventes par catégorie
            fig_pie = px.pie(
                df,
                names="category",  # Catégorie de produit
                values="total_sales",  # Valeurs des ventes totales par catégorie
                title="Répartition des Ventes par Catégorie",
                labels={"category": "Catégorie", "total_sales": "Ventes Totales (en $)"},
            )
            st.plotly_chart(fig_pie)

            # Produit le moins vendu
            bottom_category = df.loc[df['total_sales'].idxmin()]
            st.write(
                f"Catégorie la moins vendue : {bottom_category['category']} ({bottom_category['total_sales']:.2f} $)")



elif page == "Ventes par Mois":
    st.header("Analyse des Ventes Mensuelles")

    # Récupérer les données des ventes par mois
    sales_by_month_data = fetch_data("/ecommerce/sales-by-date")
    total_sales_data = fetch_data("/ecommerce/total-sales")

    if sales_by_month_data and "sales_by_date" in sales_by_month_data:
        df_monthly = pd.DataFrame(sales_by_month_data["sales_by_date"])

        if not df_monthly.empty:
            # Convertir la colonne date
            df_monthly['date'] = pd.to_datetime(df_monthly['date'])

            # Sélecteur de granularité
            granularity = st.radio(
                "Choisir la vue",
                ["Par mois", "Par année"],
                horizontal=True
            )

            # Sélecteur de période
            col_date1, col_date2 = st.columns(2)
            with col_date1:
                start_date = st.date_input(
                    "Date de début",
                    min_value=df_monthly['date'].min(),
                    max_value=df_monthly['date'].max(),
                    value=df_monthly['date'].min()
                )
            with col_date2:
                end_date = st.date_input(
                    "Date de fin",
                    min_value=df_monthly['date'].min(),
                    max_value=df_monthly['date'].max(),
                    value=df_monthly['date'].max()
                )

            # Filtrer les données selon la période sélectionnée
            mask = (df_monthly['date'] >= pd.to_datetime(start_date)) & (df_monthly['date'] <= pd.to_datetime(end_date))
            df_filtered = df_monthly.loc[mask].copy()

            # Regrouper les données selon la granularité choisie
            if granularity == "Par année":
                df_filtered['period'] = df_filtered['date'].dt.year
                period_format = lambda x: str(x)
                x_axis_title = "Année"
            else:  # Par mois
                df_filtered['period'] = df_filtered['date'].dt.strftime('%Y-%m')
                period_format = lambda x: x
                x_axis_title = "Mois"

            # Agréger les données
            df_grouped = df_filtered.groupby('period').agg({
                'total_sales': 'sum',
                'total_orders': 'sum'
            }).reset_index()
            df_grouped = df_grouped.sort_values('period')

            # Créer deux colonnes pour les graphiques
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Évolution des Ventes")
                fig_sales = px.bar(
                    df_grouped,
                    x='period',
                    y='total_sales',
                    title=f"Évolution des ventes {granularity.lower()}",
                    labels={
                        'period': x_axis_title,
                        'total_sales': 'Ventes totales ($)'
                    }
                )
                fig_sales.update_traces(marker_color='#2196F3')
                fig_sales.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_sales, use_container_width=True)

                # Statistiques des ventes sur la période sélectionnée
                total_sales = df_grouped['total_sales'].sum()
                avg_sales = df_grouped['total_sales'].mean()
                st.metric("Total des ventes sur la période", f"${total_sales:,.2f}")
                st.metric(f"Moyenne {granularity.lower()}", f"${avg_sales:,.2f}")

            with col2:
                st.subheader("Nombre de Commandes")
                fig_orders = px.bar(
                    df_grouped,
                    x='period',
                    y='total_orders',
                    title=f"Nombre de commandes {granularity.lower()}",
                    labels={
                        'period': x_axis_title,
                        'total_orders': 'Nombre de commandes'
                    }
                )
                fig_orders.update_traces(marker_color='#4CAF50')
                fig_orders.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_orders, use_container_width=True)

                # Statistiques des commandes sur la période sélectionnée
                total_orders = df_grouped['total_orders'].sum()
                avg_orders = df_grouped['total_orders'].mean()
                st.metric("Total des commandes sur la période", f"{total_orders:,}")
                st.metric(f"Moyenne {granularity.lower()}", f"{avg_orders:,.0f}")

            # Tableau détaillé
            st.subheader("Détails des ventes")
            detailed_df = df_grouped.copy()
            detailed_df = detailed_df.rename(columns={
                'period': x_axis_title,
                'total_sales': 'Ventes ($)',
                'total_orders': 'Nombre de commandes'
            })
            detailed_df['Ventes ($)'] = detailed_df['Ventes ($)'].round(2)
            st.dataframe(detailed_df.sort_values(x_axis_title, ascending=False), use_container_width=True)

        else:
            st.warning("Aucune donnée disponible pour les ventes mensuelles.")
    else:
        st.error("Erreur lors de la récupération des données mensuelles.")
