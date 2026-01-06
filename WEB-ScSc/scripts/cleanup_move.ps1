$dest = Join-Path -Path (Get-Location) -ChildPath "removed_by_cleanup\cleanup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Path $dest -Force | Out-Null
$files = @(
  'services\i18n_he.json.new','services\i18n_he.json.bak','services\i18n_he_fixed.json',
  'services\i18n_he_issues_after2.json','services\i18n_he_issues_after.json','services\i18n_he_issues.json',
  'services\i18n_extracted.json','services\i18n_english_only.csv','services\i18n_english_indexed.txt',
  'services\i18n_check_output.json','services\i18n_for_translation.csv','services\i18n_for_translation.json',
  'services\i18n.py.bak.20260104_235456','services\i18n.py.bak','services\i18n_mismatches_favorites_add.json',
  'services\i18n_mismatches_postpatch3.json','services\i18n_mismatches_postpatch2.json','services\i18n_mismatches_postpatch.json',
  'services\i18n_mismatches_after_trim.json','i18n_mismatches_full.json','i18n_mismatches.json',
  'services\i18n_text_new.json','services\i18n_ru.json.bak',
  'scripts\export_i18n_new.py','scripts\run_export_test.py','scripts\inspect_export_good.py','scripts\run_import_on_export_good.py',
  'scripts\generate_i18n_jsons.py','scripts\apply_i18n_translations.py','ExcelExamples\export_Good.xlsx'
)

foreach ($f in $files) {
  if (Test-Path $f) {
    try {
      Move-Item -Path $f -Destination $dest -Force
      Write-Output "MOVED: $f"
    } catch {
      Write-Output "ERROR moving: $f : $_"
    }
  } else {
    Write-Output "MISSING: $f"
  }
}
Write-Output "Done. Files moved to: $dest"