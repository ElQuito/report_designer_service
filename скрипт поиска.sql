create procedure dbo.ddm_reporting_service_GetSearchList
	@searchTerm nvarchar(100), -- строка поиска
	@typedata nvarchar(50) -- тип по которому производить поиск
as
begin

	set transaction isolation level read uncommitted;

	set dateformat dmy;

	set nocount on;

	-- поиск по справочнику сотрудников подразделения
	if 	@typedata = 'subdivision'
	begin

		select Name,RowID from [dbo].[dvtable_{7473F07F-11ED-4762-9F1E-7FF10808DDD1}] as RefStaff_Units where Name like '%' + @searchTerm +'%' and NotAvailable = 0;

	end;
	-- поиск по справочнику сотрудников сотрудники
	if 	@typedata = 'employees'
	begin

		select DisplayString,RowID from [dbo].[dvtable_{DBC8AE9D-C1D2-4D5E-978B-339D22B32482}] as RefStaff_Employees where DisplayString like '%' + @searchTerm +'%' and NotAvailable = 0;
		

	end;

	-- поиск по справочнику контрагентов подразделения
	if 	@typedata = 'сompanies'
	begin

		select Name,RowID from [dbo].[dvtable_{C78ABDED-DB1C-4217-AE0D-51A400546923}] as RefPartners_Companies where Name like '%' + @searchTerm +'%' and NotAvailable = 0;

	end;
	-- поиск по справочнику контрагентов сотрудники
	if 	@typedata = 'partners_employees'
	begin
		
		select isnull(LastName, '') + ' ' + isnull(FirstName,'') + ' ' + isnull(MiddleName,'') as Name,RowID from [dbo].[dvtable_{1A46BF0F-2D02-4AC9-8866-5ADF245921E8}] as RefPartners_Employees where LastName like '%' + @searchTerm +'%' and NotAvailable = 0;

	end;
	
	-- поиск по справочнику виды карточек
	if 	@typedata = 'ref_kinds_card_kinds'
	begin
		
		select Name,RowID from [dbo].[dvtable_{C7BA000C-6203-4D7F-8C6B-5CB6F1E6F851}] as RefKinds_CardKinds
			where   Name like '%' + @searchTerm +'%'
				and ParentRowID = 'E5962DFF-01D3-497B-9C3C-FBA1CEC27309' 
				and ParentTreeRowID <> '00000000-0000-0000-0000-000000000000' 
				and NotAvailable = 0;

	end;
	
	-- поиск по универсальному справочнику
	if 	@typedata = 'ref_universal_item'
	begin
		
	select 
		(select RefUniversal_ItemType.Name 
		from [dbo].[dvtable_{5E3ED23A-2B5E-47F2-887C-E154ACEAFB97}] as RefUniversal_ItemType 
		where RefUniversal_ItemType.RowID = RefUniversal_Item.ParentRowID) + ' | ' + RefUniversal_Item.Name as Name,
		RowID 
		from [dbo].[dvtable_{DD20BF9B-90F8-4D9A-9553-5B5F17AD724E}] as RefUniversal_Item
		where RefUniversal_Item.Name like '%' + @searchTerm +'%';

	end;
go