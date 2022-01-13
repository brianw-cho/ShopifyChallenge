import streamlit as st
from item_manager import ItemManager, ExistingItemException, NoSuchItemException, MissingFieldsException

st.title("Inventory Tracking System")

st.markdown("""
To create, remove, or change an item, use the sidebar menu. The ID and name of each item must be unique.
""")

@st.cache(allow_output_mutation=True)
def create_manager() -> ItemManager:
    manager = ItemManager()
    return manager


manager = create_manager()

with st.sidebar:
    with st.form("Create Items", clear_on_submit=True):
        st.header("Create Items")
        st.caption("Enter the name, ID, and number of the item to be created")

        name = st.text_input('Name')
        id = st.text_input('ID')
        num = st.number_input('Number of Item', min_value=0, step=1)

        submit = st.form_submit_button("Create Item")

        if submit:
            try:
                manager.create_item(name, id, num)
            except ExistingItemException:
                st.error("Item with the same name or ID already exists in the inventory")
            except MissingFieldsException:
                st.error("Please enter name and ID for the item")

    with st.form("Delete Items", clear_on_submit=True):
        st.header("Delete Items")
        st.caption("Enter the ID of the item to be deleted")

        id = st.text_input('ID')
        comment = st.text_input("Deletion Comment")

        submit = st.form_submit_button("Delete Item")

        if submit:
            try:
                manager.delete_item(id, comment)
            except NoSuchItemException:
                st.error("This item does not exist in the inventory")
            except MissingFieldsException:
                st.error("Please enter the ID of the item to be deleted")

    with st.form("Undelete"):
        st.header("Undelete Item")
        st.caption("The most recent deletion will be undeleted. Up to 10 undeletes can be done in a row. If there is already an item in the inventory with the same name or ID, undelete will fail.")

        submit = st.form_submit_button("Undelete")

        if submit:
            try:
                manager.undelete()
            except ExistingItemException:
                st.error("There is an item with the same name or ID in the inventory")
            except NoSuchItemException:
                st.error("No more undeletes can be made (10 max.)")

    with st.form("Edit Items", clear_on_submit=True):
        st.header("Edit Items")
        st.caption("Enter the unique ID of item to be edited along with the changed number")

        id = st.text_input('ID')
        num = st.number_input("New Number of Item", min_value=0, step=1)

        submit = st.form_submit_button("Edit Item")

        if submit:
            try:
                manager.set_num(id, num)
            except NoSuchItemException:
                st.error("This item does not exist in the inventory")
            except MissingFieldsException:
                st.error("Please enter the ID of the item to be edited")

st.markdown("""
<style>
table td:nth-child(1) {
    display: none
}
table th:nth-child(1) {
    display: none
}
</style>
""", unsafe_allow_html=True)

if not manager.is_empty():
    st.table(manager.to_dataframe())

view_deleted = st.checkbox("View Recently Deleted Items")

if view_deleted:
    st.header("Recently Deleted Items")
    if manager.is_delete():
        st.table(manager.deleted_dataframe())